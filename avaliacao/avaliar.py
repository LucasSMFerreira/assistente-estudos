import json
import sys
from pathlib import Path

from app.busca import buscar_trechos


def avaliar(k: int = 4) -> dict:
    casos = json.loads(Path("avaliacao/perguntas.json").read_text(encoding="utf-8"))
    acertos = 0
    soma_rr = 0.0
    for caso in casos:
        resultados = buscar_trechos(caso["pergunta"], k)
        for posicao, resultado in enumerate(resultados, start=1):
            if resultado["nome"] == caso["documento"] and resultado["pagina"] == caso["pagina"]:
                acertos += 1
                soma_rr += 1 / posicao
                break
    total = len(casos)
    return {
        "casos": total,
        f"acerto@{k}": round(acertos / total, 3),
        "mrr": round(soma_rr / total, 3),
    }


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print(avaliar(k))
