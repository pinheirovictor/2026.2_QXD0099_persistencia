"""Aplicação principal, servida por: uvicorn app.main:app --reload."""
import logging
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pymongo.errors import PyMongoError
from app.database import get_client
from app.routers import candidatos, estatisticas, recursos, relacionamentos

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(name)s: %(message)s')
logger = logging.getLogger('api_tse')

app = FastAPI(
    title='API TSE 2024 — Dados Abertos',
    version='0.2.0',
    description='API didática independente do TSE.',
)
app.include_router(candidatos.router)
app.include_router(relacionamentos.router)
app.include_router(recursos.router)
app.include_router(estatisticas.router)


@app.exception_handler(PyMongoError)
async def lidar_erro_banco(request: Request, exc: PyMongoError):
    logger.exception('Falha no MongoDB: %s %s', request.method, request.url.path)
    return JSONResponse(status_code=503, content={'detail': 'Banco de dados indisponível. Confira o serviço MongoDB e o .env.'})


@app.get('/', tags=['Sistema'])
def inicio():
    return {
        'mensagem': 'API TSE 2024 — dados abertos', 'versao': '0.2.0',
        'documentacao': '/docs',
        'fonte': 'https://dadosabertos.tse.jus.br/dataset/candidatos-2024',
        'colecoes': ['candidatos', 'bens', 'coligacoes', 'vagas', 'redes_sociais'],
    }


@app.get('/health', tags=['Sistema'])
def health():
    try:
        get_client().admin.command('ping')
    except PyMongoError:
        raise HTTPException(status_code=503, detail='MongoDB indisponível')
    return {'status': 'ok', 'mongodb': 'conectado'}
