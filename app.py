import time
from flask import Flask, render_template, jsonify, Response, request
import threading
import serial
from motor_control import detener_motor_2
from motor_control import mover_motor_1_forward, mover_motor_1_backward, mover_motor_2_forward, mover_motor_2_backward
from camara_control import iniciar_camara, generar_video


# Inicializa la app Flask
app = Flask(__name__)

arduino=None
PUERTO_ARDUINO = '/dev/ttyUSB0'
BAUD_RATE = 9600 

# iniciar la conexion serial qcon el Arduino
def inicializar_arduino():
    global arduino
    try:
        arduino = serial.Serial(PUERTO_ARDUINO, BAUD_RATE, timeout=1)
        time.sleep(2)  # Esperamos un momento para asegurarnos de que la conexion esta establecida
        print(f"Conexion exitosa con Arduino en {PUERTO_ARDUINO}")
    except Exception as e:
        print(f"Error al conectar con Arduino: {e}")
        arduino = None


# Rutas para controlar los motores 
@app.route('/mover_motor_1_forward')
def mover_motor_1_forward_route():
    mover_motor_1_forward()
    return jsonify({'status': 'Motor 1 movido hacia adelante'})

@app.route('/mover_motor_1_backward')
def mover_motor_1_backward_route():
    mover_motor_1_backward()
    return jsonify({'status': 'Motor 1 movido hacia atras'})

@app.route('/mover_motor_2_forward')
def mover_motor_2_forward_route():
    if mover_motor_2_forward():
        return jsonify({'status': 'motor movido hacia adelante', 'limite alcanzado': False})
    else:
        return jsonify({'status': 'Limite alcanzado', 'limite hacia direccion1': True})

@app.route('/mover_motor_2_backward')
def mover_motor_2_backward_route():
    if mover_motor_2_backward():
        return jsonify({'status': 'Motor 2 movido hacia atras', 'limite alcanzado': False})
    else:
        return jsonify({'status': 'Limite alcanzado en el movimiento hacia atras', 'limite_alcanzado': True})

@app.route('/detener_motor_2', methods=['POST'])
def detener_motor_2_endpoint():
    detener_motor_2()
    return jsonify({"status": "Motor 2 detenido"}), 200

# Ruta para el flujo de video en tiempo real
@app.route('/video_feed')
def video_feed():
    return Response(generar_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

# Funcion para iniciar la camara en un hilo separado
def iniciar_camara_en_hilo():
    iniciar_camara()


def send_to_arduino(data, tipo):
    global arduino
    if arduino and arduino.is_open:
        try:
            # Formatear el mensaje en funcion del tipo de dato
            if tipo == "altura":
                mensaje = f"r{data}\n"  # Para la altura
            elif tipo == "kp":
                mensaje = f"p{data}\n"  # Para KP
            elif tipo == "ki":
                mensaje = f"i{data}\n"  # Para KI
            elif tipo == "kd":
                mensaje = f"d{data}\n"  # Para KD
            else:
                print("Tipo de dato desconocido")
                return

            print(f"Enviando al Arduino: {mensaje}")  # Log para depuracion
            arduino.write(mensaje.encode())  # Enviar como bytes
        except Exception as e:
            print(f"Error al enviar datos al Arduino: {e}")
            raise
    else:
        print("Arduino no conectado o el puerto no este abierto. Verifica la conexion.")


# Ruta para definir altura
@app.route('/set_altura', methods=['POST'])
def set_altura():
    altura = request.form.get('altura')
    print(f"Altura recibida en Flask: {altura}")  # Imprime la altura recibida para verificar
    if altura:
        # Llamamos a la funcion de envio con la altura en formato de texto directo
        send_to_arduino(altura, "altura")
        return jsonify({'status': 'Altura recibida', 'valor': altura})
    else:
        return jsonify({'status': 'Error', 'message': 'Altura no recibida'})



@app.route('/set_p', methods=['POST'])
def set_p():
    kp = request.form.get('p')
    if kp:
        send_to_arduino(kp, "kp")  # Especifica que es el valor de KP
        return jsonify({'status': 'KP recibido', 'kp': kp})
    else:
        return jsonify({'status': 'Error', 'message': 'KP no recibido'})


@app.route('/set_i', methods=['POST'])
def set_i():
    ki = request.form.get('i')
    if ki:
        send_to_arduino(ki, "ki")  # Especifica que es el valor de KI
        return jsonify({'status': 'KI recibido', 'ki': ki})
    else:
        return jsonify({'status': 'Error', 'message': 'KI no recibido'})


@app.route('/set_d', methods=['POST'])
def set_d():
    kd = request.form.get('d')
    if kd:
        send_to_arduino(kd, "kd")  # Especifica que es el valor de KD
        return jsonify({'status': 'KD recibido', 'kd': kd})
    else:
        return jsonify({'status': 'Error', 'message': 'KD no recibido'})
 


if __name__ == '__main__':

    inicializar_arduino()

    # Iniciar la camara en un hilo separado 
    camara_thread = threading.Thread(target=iniciar_camara_en_hilo)
    camara_thread.daemon = True  
    camara_thread.start()
    

    # Iniciar la app
    app.run(host='0.0.0.0', port=5000)
