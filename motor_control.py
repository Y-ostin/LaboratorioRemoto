from gpiozero import PWMOutputDevice, OutputDevice, Button
from time import sleep
import threading

# Pines de los motores
DIR_MOTOR_1 = 23
STEP_MOTOR_1 = 24
DIR_MOTOR_2 = 22
PWM_MOTOR_2 = 27  # Usamos un pin PWM para controlar la velocidad

# Limites de carril 
LIMITE_IZQ = 16
LIMITE_DER = 26

# Configuracion del motor paso a paso (Motor 1)
motor1_dir = OutputDevice(DIR_MOTOR_1)
motor1_step = OutputDevice(STEP_MOTOR_1)

# Configuracion del motor de corriente continua (Motor 2)
motor2_dir = OutputDevice(DIR_MOTOR_2)  # Direcci�n
motor2_enable = PWMOutputDevice(PWM_MOTOR_2)  # Velocidad (PWM)

# Sensores de fin de carrera
fin_carril_izq = Button(LIMITE_IZQ, pull_up=True)
fin_carril_der = Button(LIMITE_DER, pull_up=True)



# Funci�n para mover el motor
def mover_motor(step_pin, steps, delay):
    for _ in range(steps):
        step_pin.on()
        sleep(delay)
        step_pin.off()
        sleep(delay)

# Funci�n para mover el motor con l�mites de carrera
def mover_motor_con_limite(step_pin, steps, delay, limite, direccion):
    for _ in range(steps):
        if direccion == 'izq' and fin_carril_izq.is_pressed:
            print("Limite izquierdo alcanzado. Deteniendo motor.")
            return False
        
        elif direccion == 'der' and fin_carril_der.is_pressed:
            print("Limite derecho alcanzado. Deteniendo motor.")
            return False  
        
        step_pin.on()
        sleep(delay)
        step_pin.off()
        sleep(delay)

    return True

# Funci�n en hilo para mover los motores
def motor_thread(motor_dir, motor_step, steps, delay):
    mover_motor(motor_step, steps, delay)

# Funciones p�blicas para mover los motores
def mover_motor_1_forward():
    motor1_dir.on()  # Direcci�n hacia adelante
    motor_thread_1 = threading.Thread(target=motor_thread, args=(motor1_dir, motor1_step, 200, 0.001))
    motor_thread_1.start()

def mover_motor_1_backward():
    motor1_dir.off()  # Direcci�n hacia atr�s
    motor_thread_1 = threading.Thread(target=motor_thread, args=(motor1_dir, motor1_step, 200, 0.001))
    motor_thread_1.start()

# Funciones para controlar el motor de corriente continua (Motor 2)
def mover_motor_2_forward():
    if not fin_carril_der.is_pressed:
        motor2_dir.off()  # Direcci�n hacia adelante
        motor2_enable.on()
        return {"status": "Motor 2 avanzando", "limite_alcanzado": False}
    else:
        detener_motor_2()
        return {"status": "Limite derecho alcanzado", "limite_alcanzado": True}

def mover_motor_2_backward():
    if not fin_carril_izq.is_pressed:
        motor2_dir.on()  # Direcci�n hacia atr�s
        motor2_enable.off()
        return {"status": "Motor 2 retrocediendo", "limite_alcanzado": False}
    else:
        detener_motor_2()
        return {"status": "Limite izquierdo alcanzado", "limite_alcanzado": True}

def detener_motor_2():
    motor2_enable.off()
    motor2_dir.off()  # Detener el motor (poniendo PWM en 0)
