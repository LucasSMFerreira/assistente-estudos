from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from app.ingestao import ingerir_pdf
from app.rag import responder

app = FastAPI(
    title="Assistente de Estudos",
    description=(
        "API que responde perguntas sobre PDFs de aulas usando RAG: busca os trechos mais "
        "parecidos com a pergunta (PostgreSQL + pgvector) e gera a resposta com um modelo "
        "local (Ollama), citando documento e página.\n\n"
        "Interface web: [/](/)"
    ),
    version="1.0.0",
)

PASTA_PDFS = Path("data/pdfs")
PAGINA_INICIAL = Path(__file__).parent / "static" / "index.html"


class Pergunta(BaseModel):
    pergunta: str = Field(examples=["O que é o teorema CAP?"])
    k: int = Field(default=4, ge=1, le=10, description="Quantos trechos usar como contexto")


@app.get("/", include_in_schema=False)
def inicio() -> FileResponse:
    return FileResponse(PAGINA_INICIAL)


@app.get("/health", tags=["Sistema"], summary="Verifica se a API está no ar")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/upload", tags=["Documentos"], summary="Envia e indexa um PDF")
def upload(arquivo: UploadFile) -> dict:
    if not arquivo.filename or not arquivo.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Envie um arquivo .pdf")
    PASTA_PDFS.mkdir(parents=True, exist_ok=True)
    destino = PASTA_PDFS / Path(arquivo.filename).name
    destino.write_bytes(arquivo.file.read())
    total = ingerir_pdf(destino)
    return {"documento": destino.name, "trechos": total}


@app.post("/perguntar", tags=["Perguntas"], summary="Responde com base nos PDFs, citando as fontes")
def perguntar(dados: Pergunta) -> dict:
    return responder(dados.pergunta, dados.k)