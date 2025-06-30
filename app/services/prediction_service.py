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
    # Lee el contenido binario del archivo subido.
    contents = file.file.read()
    
    # Usa Pillow para abrir la imagen y asegurarse de que esté en formato RGB.
    image = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # Redimensiona la imagen a 224x224 píxeles.
    image_resized = image.resize((224, 224))
    
    # Convierte la imagen a un array de NumPy y normaliza los píxeles (rango 0-1).
    # El resultado es un array float64/float32 por defecto, que es lo que el nuevo modelo espera.
    image_array = np.array(image_resized) / 255.0
    
    return image_array


def create_new_prediction(db: Session, file: UploadFile) -> dict:
    """
    Procesa una nueva predicción usando el modelo de producción.
    """
    # 1. Preprocesar la imagen de entrada.
    image_array = _preprocess_image(file)

    # 2. Obtener la predicción cruda del modelo llamando a nuestro cargador.
    raw_output = ModelLoader.predict(image_array)

    # 3. Interpretar la salida del modelo.
    # Si el primer elemento del array de salida es -1.0, el modelo rechazó la imagen.
    if raw_output[0] == -1.0:
        is_success = False
        predicted_class = "Imagen rechazada (No es hoja de viñedo)"
        confidence_score = 0.0
    else:
        # Si la imagen es válida, calculamos la clase y la confianza.
        is_success = True
        predicted_index = np.argmax(raw_output)
        confidence_score = float(raw_output[predicted_index])
        predicted_class = ModelLoader._class_names[predicted_index]

    # 4. Preparar los datos para guardarlos en la base de datos usando el esquema Pydantic.
    prediction_data = PredictionCreate(
        filename=file.filename,
        predicted_class=predicted_class,
        confidence_score=confidence_score,
        is_success=is_success
    )

    # 5. Guardar el resultado en la base de datos a través del repositorio.
    db_prediction = prediction_repository.create_prediction(db=db, prediction=prediction_data)
    
    return db_prediction