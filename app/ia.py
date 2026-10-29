import httpx  

from app.config import OLLAMA_URL

MODELO_EMBEDDING = "nomic-embed-text"
MODELO_CHAT = "qwen2.5:1.5b"


def gerar_embeddings(textos: list[str]) -> list[list[float]]:
    """Gera um embedding (lista de 768 números) para cada texto."""
    resposta = httpx.post(
        f"{OLLAMA_URL}/api/embed",
        json={"model": MODELO_EMBEDDING, "input": textos},
        timeout=300,
    )
    resposta.raise_for_status()
    return resposta.json()["embeddings"]


def para_vetor(embedding: list[float]) -> str:
    """Converte a lista de números no formato de texto que o pgvector entende: [0.1,0.2,...]"""
    return "[" + ",".join(str(numero) for numero in embedding) + "]"


def gerar_resposta(prompt: str) -> str:
    """Envia o prompt ao modelo de conversa e devolve o texto da resposta."""
    resposta = httpx.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": MODELO_CHAT, "prompt": prompt, "stream": False},
        timeout=600,
    )
    resposta.raise_for_status()
    return resposta.json()["response"]