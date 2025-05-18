from flask import Flask, request
app = Flask(__name__)

@app.route('/ventilador', methods=['POST'])
def controlar_ventilador():
    data = request.json
    estado = data.get('estado')  # true / false
    # Aquí enciendes/apagas el motor
    if estado:
        # digitalWrite(PIN_MOTOR, HIGH)
        pass
    else:
        # digitalWrite(PIN_MOTOR, LOW)
        pass
    return {"ok": True}
