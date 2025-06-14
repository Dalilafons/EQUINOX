import serial
import requests
import re
import time

# CONFIGURA ESTO:
PUERTO_SERIAL = 'COM9'  # Cambia esto por el COM correcto
BAUDRATE = 9600
URL_SERVIDOR = 'http://localhost:9090/sensor-data/'

# Intenta conectar con el Arduino
try:
    arduino = serial.Serial(PUERTO_SERIAL, BAUDRATE, timeout=2)
    print(f"[INFO] Conectado a {PUERTO_SERIAL}")
except Exception as e:
    print(f"[ERROR] No se pudo abrir el puerto {PUERTO_SERIAL}: {e}")
    exit()

# Bucle para leer datos y comandos
while True:
    try:
        # Leer datos del sensor desde el Arduino
        linea = arduino.readline().decode().strip()
        print(f"[SERIAL] {linea}")

        # Formato esperado: T:24.1,H:58.3
        match = re.match(r"T:(\d+\.?\d*),H:(\d+\.?\d*)", linea)
        if match:
            temperatura = float(match.group(1))
            humedad = float(match.group(2))

            payload = {
                "temperatura": temperatura,
                "humedad": humedad,
                "sensor_id": "caballeriza1"
            }

            response = requests.post(URL_SERVIDOR, json=payload)
            print(f"[POST] Código: {response.status_code} - Respuesta: {response.text}")

        # VERIFICAR SI HAY COMANDOS NUEVOS DESDE FASTAPI
        try:
            r = requests.get("http://localhost:9090/leer-comando")
            comando = r.json().get("comando", "")
            if comando:
                print(f"[COMANDO RECIBIDO] {comando}")
                # Enviamos el comando completo al Arduino
                arduino.write((comando + '\n').encode())
        except Exception as e:
            print(f"[ERROR COMANDO] {e}")

    except Exception as error:
        print(f"[ERROR GENERAL] {error}")

    time.sleep(0.5) #tiempo de mandar datos.
