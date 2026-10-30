# Assistente de Estudos com IA

![CI](https://github.com/LucasSMFerreira/assistente-estudos/actions/workflows/ci.yml/badge.svg)

Estudar por slides e PDFs de aula é lento: achar onde um conceito foi explicado exige folhear tudo.
Este projeto é uma API que responde perguntas sobre os PDFs da faculdade usando IA, sempre citando
o documento e a página de onde tirou a resposta.

![Demonstração da API respondendo uma pergunta](docs/demo.gif)

## Arquitetura

```
PDF ──► trechos ──► embeddings ──► PostgreSQL + pgvector
                                          │
Pergunta ──► embedding ──► busca por similaridade ──► trechos mais parecidos
                                                            │
                                         LLM (Ollama) ──► resposta + fontes
```

1. **Ingestão:** o PDF é lido página por página e dividido em trechos de ~800 caracteres com sobreposição.
2. **Embeddings:** cada trecho vira um vetor de 768 números (modelo `nomic-embed-text`), salvo no PostgreSQL com pgvector.
3. **Busca:** a pergunta também vira um vetor, e o banco encontra os trechos mais próximos pela distância de cosseno (índice HNSW).
4. **Resposta (RAG):** os trechos encontrados vão num prompt para o modelo `qwen2.5:1.5b`, que responde usando só esse conteúdo.

Tudo roda num **homelab próprio** (notebook antigo com Ubuntu Server), sem serviços pagos de IA.

## Tecnologias

| Área | Ferramentas |
| --- | --- |
| API | Python, FastAPI, Pydantic, Uvicorn |
| Banco de dados | PostgreSQL 17, pgvector, SQLAlchemy |
| IA | Ollama, nomic-embed-text, qwen2.5:1.5b, RAG |
| Qualidade | pytest (com mocks), ruff, GitHub Actions |
| Infraestrutura | Docker, Docker Compose, Ubuntu Server, Tailscale |

## Resultados da avaliação

Para medir a qualidade da busca, montei um conjunto de 15 perguntas com a página da resposta conhecida
e medi duas métricas: **Acerto@4** (a página certa apareceu entre os 4 primeiros resultados?) e
**MRR** (premia quando a página certa aparece mais cedo).

| Experimento | Tamanho | Sobreposição | Acerto@4 | MRR |
| --- | --- | --- | --- | --- |
| **baseline** | **800** | **100** | **0.733** | **0.7** |
| trechos pequenos | 400 | 50 | 0.733 | 0.5 |
| trechos grandes | 1200 | 150 | 0.733 | 0.5 |
| sem sobreposição | 800 | 0 | 0.733 | 0.4 |

[ESCREVA AQUI 2 OU 3 FRASES COM A SUA CONCLUSÃO. Por exemplo: o que aconteceu com o MRR quando você
mudou o tamanho dos trechos, o que a remoção da sobreposição mostrou, e qual configuração você escolheu.]

Detalhes em [docs/experimentos.md](docs/experimentos.md).

## Como rodar

Pré-requisitos: Docker e Docker Compose.

```bash
git clone https://github.com/LucasSMFerreira/assistente-estudos.git
cd assistente-estudos
cp .env.example .env              # troque a senha no arquivo
docker compose up -d              # banco e Ollama
docker compose exec ollama ollama pull nomic-embed-text
docker compose exec ollama ollama pull qwen2.5:1.5b
docker compose exec -T db psql -U estudos -d estudos < sql/001_schema.sql
docker compose exec -T db psql -U estudos -d estudos < sql/002_indice.sql
docker compose --profile prod up -d --build   # sobe a API
```

Abra `http://127.0.0.1:8000/docs`, envie um PDF em **POST /upload** e pergunte em **POST /perguntar**.

Para desenvolvimento local:

```bash
python3 -m venv .venv
source