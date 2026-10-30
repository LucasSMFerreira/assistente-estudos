def dividir_em_trechos(texto: str, tamanho: int = 800, sobreposicao: int = 100) -> list[str]:
    """Dividir o texto em trechos menores, com sobreposição entre eles."""
    if sobreposicao >= tamanho:
        raise ValueError("A sobreposição deve ser menor que o tamanho do trecho.")

    texto = " ".join(texto.split())
    trechos = []
    inicio = 0
    while inicio < len(texto):
        fim = inicio + tamanho
        trechos.append(texto[inicio:fim])
        if fim >= len(texto):
            break
        inicio += tamanho - sobreposicao
    return trechos
