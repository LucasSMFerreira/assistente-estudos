from fastapi import FastAPI

app = FastAPI(title='Assistente de Estudos')

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
