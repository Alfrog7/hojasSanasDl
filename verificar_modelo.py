import tensorflow as tf

print("--- Verificando la firma de entrada del modelo ---")

try:
    model_path = 'app/ml/modelo_final_con_validacion'
    model = tf.saved_model.load(model_path)

    # Obtenemos la firma de inferencia por defecto del modelo
    inference_signature = model.signatures['serving_default']

    # Imprimimos las especificaciones del primer tensor de entrada
    input_tensor_spec = inference_signature.inputs[0]

    print(f"Nombre de la entrada: {input_tensor_spec.name}")
    print(f"Forma esperada (shape): {input_tensor_spec.shape}")
    print(f"TIPO DE DATO ESPERADO (dtype): {input_tensor_spec.dtype}")

    if input_tensor_spec.dtype == tf.float16:
        print("\nCONFIRMADO: El modelo espera 'float16' (half). Este es el origen del error.")
    else:
        print("\nEl modelo espera 'float32'. El problema podría ser otro.")

except Exception as e:
    print(f"\nOcurrió un error al verificar el modelo: {e}")