from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import io
import numpy as np
from PIL import Image, ImageOps
from ai_edge_litert.interpreter import Interpreter
from counterfit_shims_picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)

with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())

interpreter = Interpreter(model_path='model_unquant.tflite')
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()[0]
output_details = interpreter.get_output_details()[0]

with open('labels.txt', encoding='utf-8') as labels_file:
    labels = [line.strip().split(' ', 1)[-1] for line in labels_file if line.strip()]

height, width = input_details['shape'][1:3]

image.seek(0)
picture = Image.open(image).convert('RGB')
picture = ImageOps.fit(picture, (width, height), Image.Resampling.LANCZOS)
data = np.asarray(picture, dtype=np.float32) / 127.5 - 1
data = np.expand_dims(data, axis=0)

interpreter.set_tensor(input_details['index'], data)
interpreter.invoke()
probabilities = interpreter.get_tensor(output_details['index'])[0]

for label, probability in zip(labels, probabilities):
    print(f'{label}:\t{probability * 100:.2f}%')
