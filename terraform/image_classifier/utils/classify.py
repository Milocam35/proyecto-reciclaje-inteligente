import numpy as np
from PIL import Image
from io import BytesIO
import tensorflow as tf

class ImageClassifier:
    def __init__(self, model_path="model/model_fp16.tflite"):
        """Inicializa el clasificador con TFLite"""
        print(f"Loading TFLite model from {model_path}")
        
        # Cargar el modelo TFLite usando TensorFlow
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        
        # Obtener detalles de input y output
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
        # Obtener shape esperado
        self.input_shape = self.input_details[0]['shape']
        print(f"Model loaded. Input shape: {self.input_shape}")
        
        # Clases
        self.classes = ["noReciclable", "organico", "reciclable"]

    def load_and_preprocess_image(self, image_bytes):
        """Preprocesar imagen para el modelo"""
        # Abrir imagen desde bytes
        img = Image.open(BytesIO(image_bytes))
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Redimensionar a 224x224 (o el tamaño que espere tu modelo)
        target_size = (224, 224)
        img = img.resize(target_size, Image.LANCZOS)
        
        # Convertir a array numpy
        img_array = np.array(img, dtype=np.float32)
        
        # Normalizar a [0, 1]
        img_array = img_array / 255.0
        
        # Añadir dimensión de batch: (224, 224, 3) -> (1, 224, 224, 3)
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array

    def classify(self, image_bytes):
        """Clasifica una imagen usando el modelo TFLite"""
        # Preprocesar imagen
        img = self.load_and_preprocess_image(image_bytes)  # (1,224,224,3)
        
        # Ejecutar inferencia con TFLite
        self.interpreter.set_tensor(self.input_details[0]['index'], img)
        self.interpreter.invoke()
        
        # Obtener resultado
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        preds = output_data[0]
        
        # Obtener clase y confianza
        max_index = np.argmax(preds)
        confidence = float(preds[max_index])
        label = self.classes[max_index]
        
        return label, confidence