from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.schemas.prediction_schema import PredictionCreate

# Esta capa es la única que debe interactuar directamente con el modelo de la base de datos (Prediction).
# No contiene lógica de negocio, solo operaciones de base de datos.

def create_prediction(db: Session, prediction: PredictionCreate) -> Prediction:
    """
    Crea un nuevo registro de predicción en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        prediction (PredictionCreate): El objeto con los datos de la predicción a crear.

    Returns:
        Prediction: El objeto de predicción recién creado, incluyendo el ID y la fecha generados por la BD.
    """
    # Convierte el esquema Pydantic a un diccionario y luego lo usa para crear una instancia del modelo SQLAlchemy.
    db_prediction = Prediction(**prediction.model_dump())
    
    # Añade la nueva instancia a la sesión de la base de datos.
    db.add(db_prediction)
    
    # Confirma los cambios en la base de datos (realiza el INSERT).
    db.commit()
    
    # Refresca la instancia para obtener los valores generados por la base de datos (como el 'id' y 'created_at').
    db.refresh(db_prediction)
    
    return db_prediction


def get_predictions(db: Session, skip: int = 0, limit: int = 100) -> list[Prediction]:
    """
    Obtiene una lista de registros de predicciones de la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        skip (int): El número de registros a saltar (para paginación).
        limit (int): El número máximo de registros a devolver.

    Returns:
        list[Prediction]: Una lista de objetos de predicción.
    """
    # Ejecuta una consulta para obtener todas las predicciones, aplicando paginación.
    return db.query(Prediction).offset(skip).limit(limit).all()