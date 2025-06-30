from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

# La clase Prediction representa la tabla 'predictions' en la base de datos.
# SQLAlchemy usa esta clase para mapear los objetos de Python a las filas de la tabla.

class Prediction(Base):
    """
    Modelo de la tabla de predicciones en la base de datos.
    """
    __tablename__ = "predictions"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    
    # El nombre del archivo de la imagen que se subió.
    filename = Column(String(255), nullable=False)
    
    # El resultado de la predicción del modelo (ej: "Healthy", "Black Rot").
    predicted_class = Column(String(50), nullable=False)
    
    # La puntuación de confianza de la predicción (un valor flotante entre 0 y 1).
    confidence_score = Column(Float, nullable=False)
    
    # Un booleano para saber si la predicción fue exitosa o si el modelo rechazó la imagen.
    is_success = Column(Boolean, default=True)
    
    # La fecha y hora en que se creó el registro.
    # Se establece automáticamente por la base de datos en el momento de la creación.
    created_at = Column(DateTime(timezone=True), server_default=func.now())