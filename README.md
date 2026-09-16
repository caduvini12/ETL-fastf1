# ETL FastF1 — Pipeline de Dados de Fórmula 1

Pipeline de engenharia de dados que extrai, transforma e organiza dados de telemetria e voltas de sessões de F1 (via [FastF1](https://docs.fastf1.dev/)), seguindo arquitetura em camadas (**bronze → silver → gold**), com armazenamento local e na nuvem (AWS S3), orquestrado via **Apache Airflow**.

## Resumo

- **O quê**: pipeline completo de dados de F1 — extração da API FastF1, transformação em camadas (bronze/silver/gold), armazenamento local + AWS S3, orquestração via Airflow.
- **Dado usado**: qualificação do GP de Mônaco de 2025.
- **Validação real**: o menor tempo de volta do dataset (`69.954s`, piloto NOR) bate, com precisão de milissegundo, com o recorde histórico de Lando Norris — primeira volta abaixo de 70s na história de Mônaco.
- **Insight extraído**: apesar da volta mais rápida, NOR não teve a maior velocidade média da sessão — evidência de que em Mônaco eficiência de pilotagem pesa mais que velocidade de reta.
- **Stack**: Python, pandas, FastF1, AWS S3 (boto3/s3fs), Apache Airflow, Docker Compose.

## Sumário

- [Arquitetura](#arquitetura)
- [Estrutura de pastas](#estrutura-de-pastas)
- [Stack](#stack)
- [Setup](#setup)
- [Como rodar](#como-rodar)
- [Orquestração com Airflow](#orquestração-com-airflow)
- [Análise e validação dos dados](#análise-e-validação-dos-dados)
- [Decisões de arquitetura e limitações conhecidas](#decisões-de-arquitetura-e-limitações-conhecidas)
- [Roadmap](#roadmap)

---

## Arquitetura

O pipeline segue o padrão **medallion architecture** (bronze/silver/gold), comum em engenharia de dados:

```
FastF1 API
    │
    ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│ BRONZE  │ ──▶ │ SILVER  │ ──▶ │  GOLD   │
│ (raw)   │     │(cleaned)│     │(business│
│         │     │         │     │ ready)  │
└─────────┘     └─────────┘     └─────────┘
    │                │                │
    └────────────────┴────────────────┘
                     │
                     ▼
              AWS S3 (data lake)
```

- **Bronze**: dados brutos extraídos diretamente da API do FastF1 (telemetria + dados de voltas), sem nenhuma transformação.
- **Silver**: dados limpos — conversão de unidades de tempo, renomeação de colunas para português, remoção de colunas irrelevantes.
- **Gold**: dados agregados e prontos para análise — merge entre telemetria (velocidade máxima por volta) e dados de voltas.

Cada camada é persistida tanto **localmente** (parquet, particionado por `year/place/quali`) quanto no **S3**, espelhando a mesma estrutura de pastas.

## Estrutura de pastas

```
.
├── dags/
│   └── pipeline_Fastf1.py      # DAG do Airflow
├── bronze/
│   ├── telemetry/year=.../place=.../quali=.../
│   └── Data_Laps/year=.../place=.../quali=.../
├── silver/
│   ├── telemetry/...
│   └── Data_Laps/...
├── gold/
│   └── year=.../place=.../quali=.../
├── extract.py                   # Extração da API FastF1 (camada bronze)
├── transformData.py              # Leitura + transformação bronze → silver
├── transformGold.py              # Leitura + transformação silver → gold
├── uploadS3.py                   # Upload de bronze/silver/gold para o S3
├── readingS3.py                  # Leitura de dados direto do S3 (análise)
├── docker-compose.yaml           # Ambiente Airflow (CeleryExecutor)
└── .env                          # Variáveis de ambiente (não versionado)
```

## Stack

| Camada | Ferramenta |
|---|---|
| Extração | [FastF1](https://docs.fastf1.dev/) |
| Processamento | Python, pandas |
| Armazenamento local | Parquet (fastparquet) |
| Armazenamento em nuvem | AWS S3 (boto3, s3fs) |
| Orquestração | Apache Airflow 3.3.1 (CeleryExecutor) |
| Infraestrutura | Docker Compose |

## Setup

### Pré-requisitos

- Python 3.12+
- Docker e Docker Compose
- Conta AWS com um bucket S3 criado
- Usuário IAM com permissões de `s3:PutObject`, `s3:GetObject`, `s3:ListBucket` no bucket

### 1. Clonar e instalar dependências locais

```bash
git clone <url-do-repositorio>
cd ETL-fastf1
python -m venv .venv
source .venv/bin/activate
pip install fastf1 pandas fastparquet boto3 s3fs
```

### 2. Configurar credenciais AWS

As credenciais **não são hardcoded** em nenhum lugar do código — o boto3/s3fs as localiza automaticamente via variáveis de ambiente padrão:

```bash
export AWS_ACCESS_KEY_ID="sua-chave"
export AWS_SECRET_ACCESS_KEY="sua-chave-secreta"
```

Se estiver usando **GitHub Codespaces**, configure isso como *Codespaces Secrets* (Settings → Codespaces → Secrets), em vez de exportar manualmente.

### 3. Configurar o `.env` do Airflow

Crie um arquivo `.env` na raiz do projeto (não versionado, incluído no `.gitignore`):

```
AIRFLOW_UID=50000
FERNET_KEY=
_PIP_ADDITIONAL_REQUIREMENTS=fastparquet boto3 s3fs pandas fastf1
```

> `_PIP_ADDITIONAL_REQUIREMENTS` instala as dependências do projeto dentro dos containers do Airflow. É uma solução rápida, adequada para desenvolvimento/portfólio — em produção, o correto é embutir essas dependências numa imagem Docker customizada.

## Como rodar

### Rodando localmente (sem Airflow), passo a passo

```bash
python extract.py          # gera bronze
python transformData.py    # gera silver
python transformGold.py    # gera gold
python uploadS3.py         # sobe bronze/silver/gold para o S3
```

### Rodando via Airflow (orquestrado)

```bash
docker compose up -d
```

> **Nota sobre inicialização**: em ambientes com poucos recursos, o serviço `airflow-worker` pode não subir automaticamente na primeira tentativa (fica com status `Created`, não `Up`), por depender do `airflow-apiserver` estar saudável. Se isso acontecer:
> ```bash
> docker compose up -d airflow-worker
> ```

Acesse a UI em `http://localhost:8080` (login padrão: `airflow` / `airflow`), localize a DAG `dag_fastf1_pipeline` e dispare manualmente.

## Orquestração com Airflow

A DAG (`dags/pipeline_Fastf1.py`) orquestra as etapas **a partir da camada silver**:

```
transfromSilver → transfromGold → SavingS3Bronze → SavingS3Silver → Savings3Gold
```

**A extração (bronze) roda fora da DAG, de forma manual.** Isso é uma decisão de arquitetura consciente, não uma limitação não resolvida: a API do FastF1 não responde corretamente a partir do ambiente de nuvem (GitHub Codespaces) usado para desenvolver este projeto — provavelmente por restrição de rede/IP em ambientes de datacenter. A extração é executada localmente, e os dados de bronze resultantes alimentam o restante do pipeline orquestrado.

## Análise e validação dos dados

Um dos focos deste projeto foi garantir **corretude dos dados**, não apenas movê-los de um lugar para outro. Durante o desenvolvimento, identifiquei e corrigi:

- **Inconsistência de unidade de tempo**: os campos de tempo retornados pelo FastF1 para dados de volta (`LapTime`, `Sector1Time`, etc.) estavam em nanossegundos, mas foram inicialmente tratados como microssegundos. A correção foi validada matematicamente: a soma dos três tempos de setor de cada volta bate exatamente com o tempo total da volta.
- **Validação externa**: o menor tempo de volta identificado no dataset (`69.954s`, piloto NOR, Mônaco 2025) foi conferido contra reportagem factual — Lando Norris cravou a primeira volta abaixo de 70 segundos na história de Mônaco na qualificação de 2025, com tempo de 1m9.954s. Os números batem com precisão de milissegundo.

**Insight obtido**: apesar de ter a volta mais rápida da sessão, o piloto NOR **não** teve a maior velocidade média (`VER` liderou essa métrica) — evidência de que, em Mônaco, eficiência de pilotagem em curva pesa mais que velocidade máxima de reta.

## Decisões de arquitetura e limitações conhecidas

| Decisão | Motivo |
|---|---|
| Extração fora da DAG | API do FastF1 não funciona a partir do ambiente de nuvem usado para orquestração |
| `_PIP_ADDITIONAL_REQUIREMENTS` em vez de imagem customizada | Mais rápido para portfólio/desenvolvimento; não recomendado para produção |
| `AmazonS3FullAccess` no usuário IAM | Pendente de restrição — o ideal é uma policy customizada limitada ao bucket do projeto |
| `try/except` genérico (`ValueError`) | Tratamento de erro ainda não cobre os erros reais observados em produção (`FileNotFoundError`, `NoCredentialsError`, etc.) — próximo passo de robustez |
| `CeleryExecutor` no Airflow | Configuração padrão da documentação oficial; `LocalExecutor` seria mais leve para um projeto deste porte (elimina a necessidade de Redis e do serviço worker separado) |

## Roadmap

- [ ] Restringir permissão IAM à policy mínima necessária (least privilege)
- [ ] Tratamento de erro específico por tipo de exceção real
- [ ] Migrar de `CeleryExecutor` para `LocalExecutor`
- [ ] Parametrizar a DAG para rodar qualquer combinação de ano/circuito/sessão (hoje fixo em `2025, monaco, Q`)
- [ ] Testes automatizados (unitários para as transformações, validação de schema)
- [ ] Dashboard/visualização (Metabase, Streamlit ou notebook) consumindo a camada gold direto do S3
