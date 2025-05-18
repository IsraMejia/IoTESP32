from flask import Flask, request
app = Flask(__name__)

@app.route('/Servir_Agua', methods=['POST'])
def controlar_servir_agua():
    data = request.json
    estado = data.get('estado')  # true / false
    # Aquí enciendes/apagas el motor de la bomba de agua
    if estado:
        # digitalWrite(PIN_MOTOR, HIGH)
        pass
    else:
        # digitalWrite(PIN_MOTOR, LOW)
        pass
    return {"ok": True}
