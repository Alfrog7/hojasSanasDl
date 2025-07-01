from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.database import Base

class Prediction(Base):
    """
    Modelo de la tabla de predicciones en la base de datos.
    """
    __tablename__ = "predictions"

  
    id = Column(Integer, primary_key=True, index=True)
    
  
    filename = Column(String(255), nullable=False)
    
   
    predicted_class = Column(String(50), nullable=False)
    
    
    confidence_score = Column(Float, nullable=False)
    
  
    is_success = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())