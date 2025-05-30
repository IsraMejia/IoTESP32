import socket
import json
from machine import Pin, PWM
from time import sleep

# ─── Clases de control ─────────────────────────────────────────

class VentiladorL298N:
    def __init__(self, in1_pin, in2_pin, enable_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.enable = Pin(enable_pin, Pin.OUT)

    def girar(self):
        self.enable.value(1)
        self.in1.value(0)
        self.in2.value(1)
        print("Ventilador funcionando...")

    def detener(self):
        self.in1.value(0)
        self.in2.value(0)
        self.enable.value(0)
        print("Ventilador detenido y deshabilitado.")


class BombaAgua:
    def __init__(self, in1_pin, in2_pin, enable_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.enable = Pin(enable_pin, Pin.OUT)

    def girar(self):
        self.enable.value(1)
        self.in1.value(1)
        self.in2.value(0)
        print("Bomba funcionando...")

    def detener(self):
        self.in1.value(0)
        self.in2.value(0)
        self.enable.value(0)
        print("Bomba detenida y deshabilitada.")


class ServoMotor:
    def __init__(self, control_pin):
        self.pin = Pin(control_pin)
        self.pwm = PWM(self.pin)
        self.pwm.freq(50)

    def moverAng(self, angulo, liberar=True):
        angulo = max(10, min(angulo, 170))
        duty = int(1638 + (angulo / 180) * (8191 - 1638))
        self.pwm.duty_u16(duty)
        print(f"Servo movido a {angulo} grados.")
        sleep(0.2)
        if liberar:
            self.liberar()

    def liberar(self):
        self.pwm.duty_u16(0)
        print("Servo liberado (sin tensión).")

# ─── Instancias físicas ───────────────────────────────────────

ventilador = VentiladorL298N(in1_pin=25, in2_pin=26, enable_pin=27)
bomba = BombaAgua(in1_pin=13, in2_pin=12, enable_pin=14)
aspersor = ServoMotor(control_pin=18)
puerta = ServoMotor(control_pin=32)

buzzer = Pin(23, Pin.OUT)                  
boton = Pin(22, Pin.IN, Pin.PULL_UP)  

puerta_abierta = False

# ─── Manejo de rutas HTTP ─────────────────────────────────────

def manejar_peticion(path, body):
    global puerta_abierta
    try:
        data = json.loads(body)
        estado = data.get("estado", False)

        if path == '/ventilador':
            ventilador.girar() if estado else ventilador.detener()
            return {"status": "ok", "mensaje": "Ventilador actualizado"}

        elif path == '/bomba':
            bomba.girar() if estado else bomba.detener()
            return {"status": "ok", "mensaje": "Bomba actualizada"}

        elif path == '/atomizador':
            if estado:
                for _ in range(3):
                    aspersor.moverAng(180, liberar=False)
                    sleep(0.5)
                    aspersor.moverAng(40, liberar=False)
                    sleep(0.5)
                aspersor.liberar()
            return {"status": "ok", "mensaje": "Atomizador activado"}

        elif path == '/puerta':
            if estado:
                puerta.moverAng(50)
                puerta_abierta = True
                print("Puerta abierta.")
            else:
                puerta.moverAng(160)
                puerta_abierta = False
                print("Puerta cerrada.")
            return {"status": "ok", "mensaje": "Puerta actualizada"}

        elif path == '/alarma':
            if estado:
                print("⏳ Esperando 10 segundos antes de sonar alarma...")
                sleep(10)

                print("🔊 Activando alarma...")
                ventilador.girar()
                buzzer.value(1)

                for _ in range(3):  # Movimiento rápido 3 veces del aspersor
                    aspersor.moverAng(180, liberar=False)
                    aspersor.moverAng(40, liberar=False)

                print("⌛ Esperando presionar el botón para detener alarma...")
                while boton.value() == 1:
                    pass

                print("👆 Botón presionado. Deteniendo alarma...")
                buzzer.value(0)
                ventilador.detener()
                aspersor.liberar()

                print("💧 Sirviendo agua por 5 segundos...")
                bomba.girar()
                sleep(5)
                bomba.detener()
                print("✅ Alarma finalizada")

            return {"status": "ok", "mensaje": "Alarma procesada"}

        else:
            return {"status": "error", "mensaje": "Ruta no válida"}

    except Exception as e:
        print("❌ Error en manejo de petición:", e)
        return {"status": "error", "mensaje": str(e)}

# ─── Servidor HTTP ─────────────────────────────────────────────

def iniciar_servidor():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(addr)
    except OSError as e:
        print("⚠️ Error al bindear socket:", e)
        return
    s.listen(1)
    print("🚀 Servidor HTTP en puerto 80...")

    while True:
        try:
            cl, addr = s.accept()
            print('📡 Conexión desde', addr)
            request = cl.recv(1024).decode()
            headers, _, body = request.partition('\r\n\r\n')
            try:
                method, path, _ = headers.split('\n')[0].split()
            except ValueError:
                cl.send('HTTP/1.0 400 Bad Request\r\n\r\n')
                cl.send('{"status":"error","mensaje":"Encabezado mal formado"}')
                cl.close()
                continue

            respuesta = manejar_peticion(path, body) if method == 'POST' else {"status": "error", "mensaje": "Método no soportado"}

            cl.send('HTTP/1.0 200 OK\r\nContent-Type: application/json\r\n\r\n')
            cl.send(json.dumps(respuesta))
            cl.close()

        except Exception as e:
            print('❌ Error en la conexión:', e)
            continue

# ─── MAIN ──────────────────────────────────────────────────────

iniciar_servidor()