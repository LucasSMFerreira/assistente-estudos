import pytest

from app.trechos import dividir_em_trechos


def test_texto_curto_vira_um_trecho():
    assert dividir_em_trechos("olá mundo") == ["olá mundo"]


def test_texto_vazio_nao_gera_trechos():
    assert dividir_em_trechos("") == []


def test_espacos_extras_sao_removidos():
    assert dividir_em_trechos("a   b\n\nc") == ["a b c"]


def test_trechos_tem_sobreposicao():
    texto = "a" * 100 + "b" * 100
    trechos = dividir_em_trechos(texto, tamanho=120, sobreposicao=20)
    assert len(trechos) == 2
    assert trechos[0][-20:] == trechos[1][:20]


def test_sobreposicao_invalida_gera_erro():
    with pytest.raises(ValueError):
        dividir_em_trechos("abc", tamanho=10, sobreposicao=10)