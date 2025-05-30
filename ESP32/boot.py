# boot.py – Configura WiFi al arranque
import network
 
ssid = 'raspberry_25'
password = 'NnpQuN6LCHbm' 

def conectar_wifi(): 
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    ip = '192.168.0.60'
    subnet = '255.255.255.0'
    gateway = '192.168.0.1'
    dns = '8.8.8.8'

    wlan.ifconfig((ip, subnet, gateway, dns))
    wlan.connect(ssid, password)

    print("🔌 Conectando WiFi desde boot.py...") 
    while not wlan.isconnected():
        pass

    print("✅ WiFi conectada:", wlan.ifconfig())

conectar_wifi()

