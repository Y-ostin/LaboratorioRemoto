from gpiozero import OutputDevice
from time import sleep
from flask import Flask, render_template, jsonify

# Definir pines de los motores
DIR_MOTOR_1 = 23
STEP_MOTOR_1 = 24
DIR_MOTOR_2 = 22
STEP_MOTOR_2 = 27

motor1_dir = OutputDevice(DIR_MOTOR_1)
motor1_step = OutputDevice(STEP_MOTOR_1)

motor2_dir = OutputDevice(DIR_MOTOR_2)
motor2_step = OutputDevice(STEP_MOTOR_2)

# Funci�n para mover los motores
def mover_motor(step_pin, steps, delay):
    for _ in range(steps):
        step_pin.on()
        sleep(delay)
        step_pin.off()
        sleep(delay)

# Configurar la aplicaci�n Flask
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mover_motor_1_forward')
def mover_motor_1_forward():
    motor1_dir.on()  # Direcci�n hacia adelante
    mover_motor(motor1_step, 200, 0.001)  # Mover motor 1
    return jsonify({'status': 'Motor 1 movido hacia adelante'})

@app.route('/mover_motor_1_backward')
def mover_motor_1_backward():
    motor1_dir.off()  # Direcci�n hacia atr�s
    mover_motor(motor1_step, 200, 0.001)  # Mover motor 1
    return jsonify({'status': 'Motor 1 movido hacia atr�s'})

@app.route('/mover_motor_2_forward')
def mover_motor_2_forward():
    motor2_dir.on()  # Direcci�n hacia adelante
    mover_motor(motor2_step, 200, 0.001)  # Mover motor 2
    return jsonify({'status': 'Motor 2 movido hacia adelante'})

@app.route('/mover_motor_2_backward')
def mover_motor_2_backward():
    motor2_dir.off()  # Direcci�n hacia atr�s
    mover_motor(motor2_step, 200, 0.001)  # Mover motor 2
    return jsonify({'status': 'Motor 2 movido hacia atr�s'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
