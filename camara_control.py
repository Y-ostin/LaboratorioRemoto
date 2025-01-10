import signal
import sys
import cv2
import threading
from flask import Response
import time

# Variable global para la camara
cap = None

# Inicia camara en hilo separado
def iniciar_camara():
    global cap
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        raise Exception("No se pudo abrir la camara")
    
    cap.set(cv2.CAP_PROP_FPS, 30)  # 30 FPS 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Ancho de fotograma
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Alto de fotograma

# Genera video
def generar_video():
    global cap
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convierte imagen a jpeg
        ret, jpeg = cv2.imencode('.jpg', frame)
        if not ret:
            break

        # Enviar el fotograma como byte stream
        frame_data = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_data + b'\r\n\r\n')

# Detener la camara 
def detener_camara():
    global cap
    if cap is not None and cap.isOpened():
        cap.release()
    sys.exit(0)


