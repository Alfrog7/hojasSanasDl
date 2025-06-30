import tensorflow as tf
import numpy as np

class ModelLoader:
    """
    Clase Singleton para cargar el modelo de producción (formato SavedModel float32).
    """
    _model_layer = None
    _class_names = ['Black Rot', 'Downy Mildew', 'Esca', 'Healthy', 'Leaf Blight']

    @classmethod
    def get_model_layer(cls):
        """
        Carga el modelo como una capa de inferencia si aún no ha sido cargado.
        """
        if cls._model_layer is None:
            # Apunta a la carpeta del modelo que ahora contiene la versión float32.
            model_path = 'app/ml/modelo_final_con_validacion'
            
            # Carga la capa de inferencia desde el directorio del SavedModel.
            cls._model_layer = tf.keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')
            
            print("Modelo de producción (float32) cargado exitosamente.")
        return cls._model_layer

    @classmethod
    def predict(cls, image_array: np.ndarray) -> np.ndarray:
        """
        Realiza una predicción usando la capa del modelo cargado.
        """
        model_layer = cls.get_model_layer()
        
        # El modelo espera un "batch" de imágenes, así que añadimos una dimensión.
        image_batch = np.expand_dims(image_array, axis=0)
        
        # Llama a la capa del modelo directamente. No se necesita ninguna conversión
        # de tipo de dato, ya que tanto la imagen como el modelo usan float32.
        prediction_dict = model_layer(image_batch)
        
        # La salida del modelo es un diccionario, extraemos el tensor por su clave.
        raw_output = prediction_dict['output_0'].numpy()[0]
        
        return raw_output