from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def hello():
    return {"mensagem": "Olá mundo lindo!"}
