from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_retorna_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_perguntar_devolve_resposta_e_fontes(monkeypatch):
    def responder_falso(pergunta, k):
        return {"resposta": "Resposta de teste", "fontes": []}

    monkeypatch.setattr("app.main.responder", responder_falso)
    resposta = client.post("/perguntar", json={"pergunta": "O que é CAP?"})
    assert resposta.status_code == 200
    assert resposta.json()["resposta"] == "Resposta de teste"


def test_perguntar_sem_pergunta_da_erro_422():
    resposta = client.post("/perguntar", json={})
    assert resposta.status_code == 422


def test_upload_rejeita_arquivo_que_nao_e_pdf():
    resposta = client.post("/upload", files={"arquivo": ("nota.txt", b"oi", "text/plain")})
    assert resposta.status_code == 400
