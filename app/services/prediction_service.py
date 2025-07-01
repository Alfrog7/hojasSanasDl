from fastapi import UploadFile
from sqlalchemy.orm import Session
from PIL import Image
import numpy as np
import io

from app.schemas.prediction_schema import PredictionCreate
from app.repository import prediction_repository
from app.ml.model_loader import ModelLoader

def _preprocess_image(file: UploadFile) -> np.ndarray:
    """
    Lee una imagen, la preprocesa y la prepara para el modelo.
    """

    contents = file.file.read()
    
   
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
   
    image_resized = image.resize((224, 224))
    
   
    image_array = np.array(image_resized) / 255.0
    
    return image_array


def create_new_prediction(db: Session, file: UploadFile) -> dict:
    """
    Procesa una nueva predicción usando el modelo de producción.
    """
  
    image_array = _preprocess_image(file)

    
    raw_output = ModelLoader.predict(image_array)

   
    if raw_output[0] == -1.0:
        is_success = False
        predicted_class = "Imagen rechazada (No es hoja de viñedo)"
        confidence_score = 0.0
    else:
       
        is_success = True
        predicted_index = np.argmax(raw_output)
        confidence_score = float(raw_output[predicted_index])
        predicted_class = ModelLoader._class_names[predicted_index]


    prediction_data = PredictionCreate(
        filename=file.filename,
        predicted_class=predicted_class,
        confidence_score=confidence_score,
        is_success=is_success
    )

    
    db_prediction = prediction_repository.create_prediction(db=db, prediction=prediction_data)
    
    return db_prediction