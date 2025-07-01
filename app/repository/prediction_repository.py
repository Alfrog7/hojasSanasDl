from sqlalchemy.orm import Session
from app.models.prediction import Prediction
from app.schemas.prediction_schema import PredictionCreate


def create_prediction(db: Session, prediction: PredictionCreate) -> Prediction:
    """
    Crea un nuevo registro de predicción en la base de datos.

    Args:
        db (Session): La sesión de la base de datos.
        prediction (PredictionCreate): El objeto con los datos de la predicción a crear.

    Returns:
        Prediction: El objeto de predicción recién creado, incluyendo el ID y la fecha generados por la BD.
    """

    db_prediction = Prediction(**prediction.model_dump())
    

    db.add(db_prediction)
 
    db.commit()
    

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

    return db.query(Prediction).offset(skip).limit(limit).all()