from fastapi import FastAPI
from app.routers import prediction_router
from app.db.database import engine, Base


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="API de Clasificación de Hojas de Vid",
    description="Una API para clasificar la salud de las hojas de vid usando un modelo de Deep Learning.",
    version="0.1.0"
)


app.include_router(prediction_router.router)


@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz para verificar que la API está funcionando."""
    return {"message": "Bienvenido a la API de Clasificación de Hojas de Vid"}