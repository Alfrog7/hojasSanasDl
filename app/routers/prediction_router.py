from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.prediction_schema import Prediction
from app.services import prediction_service

router = APIRouter(
    prefix="/predict",
    tags=["Predictions"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Prediction, status_code=status.HTTP_201_CREATED)
async def run_prediction(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Recibe una imagen de hoja de vid, ejecuta la predicción y guarda el resultado.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El archivo subido no es una imagen."
        )

    # --- LÍNEA CORREGIDA ---
    # Ahora pasamos el objeto 'file' completo, que es lo que el servicio espera.
    prediction_result = prediction_service.create_new_prediction(db=db, file=file)
    # -----------------------

    if not prediction_result:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo crear el registro de la predicción."
        )

    return prediction_result