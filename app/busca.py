from sqlalchemy import text

from app.db import engine
from app.ia import gerar_embeddings, para_vetor

SQL_BUSCA = text(
    """
    SELECT d.nome, t.pagina, t.conteudo,
           1 - (t.embedding <=> CAST(:vetor AS vector)) AS similaridade
    FROM trechos t
    JOIN documentos d ON d.id = t.documento_id
    ORDER BY t.embedding <=> CAST(:vetor AS vector)
    LIMIT :k
    """
)


def buscar_trechos(pergunta: str, k: int = 4) -> list[dict]:
    """Retorna os k trechos com significado mais parecido com a pergunta."""
    vetor = para_vetor(gerar_embeddings([pergunta])[0])
    with engine.connect() as conn:
        linhas = conn.execute(SQL_BUSCA, {"vetor": vetor, "k": k}).mappings().all()
    return [dict(linha) for linha in linhas]