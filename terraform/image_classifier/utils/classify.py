import numpy as np
from utils.preprocess import load_and_preprocess_image
import tflite_runtime.interpreter as tflite

class ImageClassifier:
    def __init__(self, model_path="model/model_fp16.tflite"):
        # cargar modelo TFLite
        self.interpreter = tflite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()

        # obtener detalles de entrada/salida
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.classes = ["reciclable", "noReciclable", "organico"]

    def classify(self, image_bytes):
        # preprocesar imagen
        img = load_and_preprocess_image(image_bytes)

        # configurar entrada
        self.interpreter.set_tensor(self.input_details[0]['index'], img)

        # ejecutar inferencia
        self.interpreter.invoke()

        # obtener salida
        predictions = self.interpreter.get_tensor(self.output_details[0]['index'])[0]

        max_index = np.argmax(predictions)
        confidence = float(predictions[max_index])
        label = self.classes[max_index]

        return label, confidence
