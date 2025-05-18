import network
import socket
import json
from machine import Pin, PWM
import time

# Servo conectado al pin GPIO14
servo = PWM(Pin(14), freq=50)

# Función para mover el servo (ajustar duty según tu servo)
def mover_atomizador(activar):
    if activar:
        for _ in range(3):
            servo.duty(120)  # posición de activación
            time.sleep(0.5)
            servo.duty(40)   # posición de reposo
            time.sleep(0.5)
    else:
        servo.duty(40)  # reposo definitivo

# Conexión WiFi
ssid = 'TU_SSID'
password = 'TU_PASSWORD'

def conectar_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print('WiFi conectada:', wlan.ifconfig())

def manejar_peticion(path, body):
    try:
        data = json.loads(body)
        estado = data.get("estado", False)

        if path == '/atomizador':
            mover_atomizador(estado)
            return "Atomizador movido"
        else:
            return "Ruta no válida"
    except Exception as e:
        return f"Error: {e}"

def iniciar_servidor():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("Servidor HTTP en puerto 80...")

    while True:
        cl, addr = s.accept()
        print('Conexión desde', addr)
        request = cl.recv(1024).decode()
        headers, _, body = request.partition('\r\n\r\n')
        method, path, _ = headers.split('\n')[0].split()

        if method == 'POST':
            respuesta = manejar_peticion(path, body)
        else:
            respuesta = "Método no soportado"

        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/plain\r\n\r\n')
        cl.send(respuesta)
        cl.close()

# MAIN
conectar_wifi()
iniciar_servidor()
