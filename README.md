# 🧠 ESP32 Domótica Inteligente - MicroPython

Este repositorio contiene el código fuente necesario para ejecutar un servidor HTTP embebido en una tarjeta ESP32 programada con MicroPython. Esta ESP32 forma parte de un sistema completo de domótica local controlado por una app Flutter y un backend FastAPI, donde se controlan dispositivos como ventiladores, bomba de agua, aspersores, buzzer y puerta automatizada.

## 🧠 Autores

- Mejía Alba Israel Hipólito  
- Ruiz Gaspar José Ángel

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.


## 🚀 Descripción del proyecto

El microcontrolador ESP32 actúa como un servidor HTTP que escucha en el puerto 80. Recibe peticiones POST desde el backend, cada una con una estructura JSON del tipo `{"estado": true}` para activar o desactivar un dispositivo específico.

El código está organizado en dos archivos principales:

- `boot.py`: Configura la conexión Wi-Fi del ESP32 con IP estática.
- `main.py`: Contiene el servidor HTTP y la lógica de control para los dispositivos conectados.

### 🌐 Rutas HTTP disponibles

| Ruta          | Dispositivo Controlado    | Descripción                                                  |
|---------------|---------------------------|--------------------------------------------------------------|
| `/ventilador` | Motor de ventilador       | Enciende o apaga el ventilador mediante puente H (L298N).   |
| `/bomba`      | Bomba de agua 12V         | Activa la bomba por 5 segundos.                             |
| `/atomizador` | Servomotor de aspersor    | Realiza 3 ciclos rápidos de rociado.                        |
| `/puerta`     | Servomotor de puerta      | Abre o cierra la puerta mediante ángulos específicos.       |
| `/alarma`     | Buzzer, ventilador, atomizador, bomba | Inicia la rutina de alarma física.            |

## 🔌 Requisitos de conexión

- Wi-Fi local compartido con el backend y la app Flutter.
- IP estática configurada en `boot.py`.
- Pines GPIO predefinidos para cada dispositivo.

## 📂 Estructura del repositorio

```
esp32/
│
├── boot.py        # Conexión Wi-Fi
├── main.py        # Servidor HTTP y lógica de dispositivos
└── README.md      # Este archivo
```

## 🤖 Dispositivos controlados

- Ventilador 5V (control digital)
- Bomba de agua 12V (control con L298N)
- Servomotor para atomizador (PWM)
- Servomotor para puerta (PWM)
- Buzzer pasivo (control digital)
- Botón físico para apagar alarma (GPIO IN)

