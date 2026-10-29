from app.busca import buscar_trechos
from app.ia import gerar_resposta

PROMPT = """Você é um assistente de estudos. Responda à pergunta usando SOMENTE os trechos abaixo.
Se a resposta não estiver nos trechos, diga que não encontrou no material.
Responda em português, de forma clara e curta.

Trechos:
{contexto}

Pergunta: {pergunta}
Resposta:"""


def responder(pergunta: str, k: int = 4) -> dict:
    """Busca os trechos, monta o prompt e devolve a resposta com as fontes."""
    trechos = buscar_trechos(pergunta, k)
    contexto = "\n\n".join(
        f"[{t['nome']}, página {t['pagina']}] {t['conteudo']}" for t in trechos
    )
    resposta = gerar_resposta(PROMPT.format(contexto=___, pergunta=pergunta))
    fontes = [
        {
            "documento": t["nome"],
            "pagina": t["pagina"],
            "similaridade": round(t["similaridade"], 3),
        }
        for t in trechos
    ]
    return {"resposta": resposta, "fontes": fontes}