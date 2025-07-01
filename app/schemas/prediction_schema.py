from pydantic import BaseModel
from datetime import datetime


class PredictionBase(BaseModel):
    """
    Esquema base con los campos comunes para una predicción.
    """
    filename: str
    predicted_class: str
    confidence_score: float
    is_success: bool


class PredictionCreate(PredictionBase):
    """
    Esquema utilizado para crear una nueva predicción en la base de datos.
    Hereda todos los campos de PredictionBase. En este caso, no añade campos nuevos.
    """
    pass


class Prediction(PredictionBase):
    """
    Esquema utilizado para devolver una predicción desde la API.
    Hereda de PredictionBase y añade los campos que son generados por la base de datos.
    """
    id: int
    created_at: datetime

    class Config:
    
        from_attributes = True