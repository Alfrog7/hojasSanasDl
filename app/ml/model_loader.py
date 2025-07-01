import tensorflow as tf
import numpy as np
import cv2

class ModelLoader:
    """
    Clase Singleton para cargar el modelo base entrenado con validación de dominio.
    """
    _model = None
    _class_names = ['Black Rot', 'Downy Mildew', 'Esca', 'Healthy', 'Leaf Blight']

    @classmethod
    def get_model(cls):
        """
        Carga el modelo base entrenado (archivo .h5).
        """
        if cls._model is None:
            model_path = 'app/ml/best_model_weights.h5'
            

            class Cast(tf.keras.layers.Layer):
                def __init__(self, dtype, **kwargs):
                    super(Cast, self).__init__(**kwargs)
                    self._dtype = dtype

                def call(self, inputs):
                    return tf.cast(inputs, self._dtype)

                def get_config(self):
                    config = super(Cast, self).get_config()
                    config.update({"dtype": self._dtype.name})
                    return config
            
            
            cls._model = tf.keras.models.load_model(
                model_path, 
                custom_objects={'Cast': Cast}
            )
            
            print("Modelo base cargado exitosamente.")
        return cls._model

    @classmethod
    def predict(cls, image_array: np.ndarray) -> np.ndarray:
        """
        Realiza predicción con validación de dominio implementada en Python.
        """
        model = cls.get_model()
        
      
        image_batch = np.expand_dims(image_array, axis=0)
        
      
        predictions = model.predict(image_batch, verbose=0)
        raw_output = predictions[0]
        
   
        is_valid = cls._validate_image_domain(image_array, raw_output)
        
        if not is_valid:
           
            return np.array([-1.0, -1.0, -1.0, -1.0, -1.0])
        else:
          
            return raw_output
    
    @classmethod
    def _validate_image_domain(cls, image_array: np.ndarray, predictions: np.ndarray) -> bool:
        """
        Validación de dominio implementada en Python puro.
        
        Verifica:
        1. Confianza del modelo > 50% (más estricto)
        2. Presencia de color verde específico > 20% (más estricto)
        3. Forma típica de hoja (aspect ratio y bordes)
        """
        
        confidence = np.max(predictions)
        has_confidence = confidence > 0.5  
        
       
        image_uint8 = (image_array * 255).astype(np.uint8)
        hsv = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2HSV)
        
       
        lower_green = np.array([35, 40, 40])   
        upper_green = np.array([85, 255, 255]) 
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        
        green_ratio = np.sum(green_mask > 0) / (224 * 224)
        has_green_color = green_ratio > 0.2  
        
       
        gray = cv2.cvtColor(image_uint8, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_ratio = np.sum(edges > 0) / (224 * 224)
        has_leaf_structure = edge_ratio > 0.05  
        
       
        hsv_face_lower = np.array([0, 20, 70])  
        hsv_face_upper = np.array([20, 255, 255])
        face_mask = cv2.inRange(hsv, hsv_face_lower, hsv_face_upper)
        face_ratio = np.sum(face_mask > 0) / (224 * 224)
        is_not_face = face_ratio < 0.3  
        
   
        return has_confidence and has_green_color and has_leaf_structure and is_not_face