import sys
from pathlib import Path

from sqlalchemy import text

from app.db import engine
from app.pdf import ler_pdf
from app.trechos import dividir_em_trechos


def ingerir_pdf(caminho: Path) -> int:
    """Lê o PDF, divide em trechos e salva no banco. Retorna quantos trechos salvou."""
    paginas = ler_pdf(caminho)
    total = 0
    with engine.begin() as conn:
        documento_id = conn.execute(
            text(
                "INSERT INTO documentos (nome) VALUES (:nome) "
                "ON CONFLICT (nome) DO UPDATE SET nome = EXCLUDED.nome RETURNING id"
            ),
            {"nome": caminho.name},
        ).scalar_one()
        conn.execute(
            text("DELETE FROM trechos WHERE documento_id = :id"),
            {"id": documento_id},
        )
        for numero, texto_pagina in enumerate(paginas, start=1):
            for trecho in dividir_em_trechos(texto_pagina):
                conn.execute(
                    text(
                        "INSERT INTO trechos (documento_id, pagina, conteudo) "
                        "VALUES (:documento_id, :pagina, :conteudo)"
                    ),
                    {"documento_id": documento_id, "pagina": numero, "conteudo": trecho},
                )
                total += 1
    return total


if __name__ == "__main__":
    quantidade = ingerir_pdf(Path(sys.argv[1]))
    print(f"{quantidade} trechos salvos")