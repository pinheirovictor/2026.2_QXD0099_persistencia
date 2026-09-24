import logging
import os
import time

from fastapi import FastAPI, Request

from database import create_db_and_tables, create_engine
from routers import pacientes, medicos, especialidades, consultas


logging.basicConfig(
    level=logging.INFO,
    format= "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("Clinica")

app = FastAPI(
    title="ClinicaAPI",
    version="1.0.0",
    description="API para uma clinica médica"
)

@app.on_event("startup")
def startup():
    create_db_and_tables()
    

@app.middleware("http")
async def registrar_requisicoes(request: Request, call_next):
    inicio = time.perf_counter()
    
    response = await call_next(request)
    
    duracao_ms = (time.perf_counter() - inicio) * 1000 
    
    logger.info(
        "%s, %s -> %s | %.2f ms",
        request.method,
        request.url.path,
        response.status_code,
        duracao_ms
    )
    
    return response


app.include_router(pacientes.router)
app.include_router(medicos.router)
app.include_router(especialidades.router)
app.include_router(consultas.router)





