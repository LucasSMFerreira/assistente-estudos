Assistente de Estudos com IA
API que responde perguntas sobre PDFs de aulas usando RAG
(FastAPI, PostgreSQL + pgvector e Ollama), rodando num homelab próprio.

Como rodar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload