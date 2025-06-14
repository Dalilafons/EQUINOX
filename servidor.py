import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="EQUINOX - Angelo", version="1.0.0")

# Permitir acceso desde otras apps (como Arduino)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para los datos recibidos
class SensorData(BaseModel):
    temperatura: float
    humedad: float
    sensor_id: str

# Guardar último dato
ultimo_dato = {}

# Guardar el último comando enviado desde la interfaz
ultimo_comando = ""

nivel_bebedero = 0  # valor por defecto

@app.post("/sensor-data/")
async def recibir_datos(data: SensorData):
    global ultimo_dato
    ultimo_dato = data.dict()
    ultimo_dato["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"message": "Datos recibidos correctamente", "data": ultimo_dato}

@app.get("/", response_class=HTMLResponse)
async def pagina_principal():
    return """
    <html>
        <head>
            <title>EQUINOX</title>
            <style>
                body {
                    background-image: url('https://i.pinimg.com/originals/ef/68/f2/ef68f211a53b53c952a1445c16dcab6b.jpg');
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    color: white;
                    margin: 0;
                    padding: 0;
                }
                .container {
                    background-color: rgba(0, 0, 0, 0.5);
                    margin: 50px auto;
                    padding: 40px;
                    border-radius: 15px;
                    width: 80%;
                    max-width: 600px;
                }
                h1 {
                    font-size: 32px;
                    margin-bottom: 30px;
                }
                h2 {
                    font-size: 20px;
                    margin-top: 25px;
                    margin-bottom: 10px;
                }
                button, a {
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 10px;
                    margin: 8px;
                    text-decoration: none;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                hr {
                    border: none;
                    height: 2px;
                    background-color: white;
                    margin: 30px 0;
                }
                .dispensador {
                    background-color: #e67e22;
                    color: white;
                }
                .dispensador:hover {
                    background-color: #d35400;
                }
                .abrir {
                    background-color: #58d68d;
                    color: black;
                }
                .abrir:hover {
                    background-color: #27ae60;
                }
                .cerrar {
                    background-color: #ff6b6b;
                    color: white;
                }
                .cerrar:hover {
                    background-color: #c0392b;
                }
                .visualizar {
                    background-color: #d4ac0d;
                    color: white;
                }
                .visualizar:hover {
                    background-color: #d68910;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Bienvenido a EQUINOX</h1>
                <hr>

                <h2>Control de dispensador de agua y comida</h2>
                <a href="/control_de_dispensador">
                    <button class="dispensador">Dispensadores</button>
                </a>
                <hr>

                <h2>Control de acceso - Puerta</h2>
                <button class="abrir" onclick="enviarComando('puerta_abierta')">Abrir</button>
                <button class="cerrar" onclick="enviarComando('puerta_cerrada')">Cerrar</button>

                <script>
                    async function enviarComando(valor) {
                        await fetch(`/enviar/${valor}`);
                        alert("Comando enviado: " + valor);
                    }
                </script>

                <hr>

                <h2>Visualización de los sensores</h2>
                <a href="/visualizar">
                    <button class="visualizar">Visualizar</button>
                </a>
            </div>
        </body>
    </html>
    """

@app.get("/visualizar", response_class=HTMLResponse)
async def visualizar_datos():
    return """
    <html>
        <head>
            <title>Control del ambiente - EQUINOX</title>
            <link href="https://fonts.googleapis.com/css2?family=Handlee&display=swap" rel="stylesheet">
            <script>
                async function actualizarDatos() {
                    const response = await fetch('/api/ultimo-dato');
                    const data = await response.json();
                    document.getElementById("humedad").innerText = data.humedad + " %";
                    document.getElementById("temperatura").innerText = data.temperatura + " °C";
                }

                setInterval(actualizarDatos, 3000);
                window.onload = actualizarDatos;
            </script>
            <style>
                body {
                    background-image: url('https://i.pinimg.com/originals/ef/68/f2/ef68f211a53b53c952a1445c16dcab6b.jpg');
                    background-size: cover;
                    background-position: center;
                    font-family: Arial, sans-serif;
                    color: white;
                    text-align: center;
                }
                .container {
                    background-color: rgba(0, 0, 0, 0.5);
                    margin: 50px auto;
                    padding: 40px;
                    border-radius: 15px;
                    width: 80%;
                    max-width: 600px;
                }
                
                h1 {
                    margin-bottom: 40px;
                    font-size: 28px;
                    color: white;
                }

                .row {
                    display: flex;
                    justify-content: space-around;
                    align-items: center;
                    gap: 20px;
                    flex-wrap: wrap;
                }

                .sensor {
                    flex: 1;
                    min-width: 200px;
                    text-align: center;
                }

                .sensor img {
                    width: 80px;
                    height: 80px;
                    margin-bottom: 10px;
                }

                .label {
                    font-size: 20px;
                    font-weight: bold;
                    color: #3498db;
                    margin-bottom: 5px;
                }

                .value {
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                }

                .boton-regresar {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border: none;
                border-radius: 10px;
                cursor: pointer;
                margin-top: 20px;
                transition: background-color 0.3s;
                }

                .boton-regresar:hover {
                    background-color: #2980b9;
                }

            </style>
        </head>
        <body>
            <div class="container">
                <h1>Control del ambiente <br> de la caballeriza</h1>

                <div class="row">
                    <div class="sensor">
                        <img src="https://cdn-icons-png.flaticon.com/512/3262/3262966.png" alt="Humedad">
                        <div class="label">Humedad</div>
                        <div class="value" id="humedad">-- %</div>
                    </div>
                    <div class="sensor">
                        <img src="https://cdn-icons-png.flaticon.com/512/566/566522.png" alt="Temperatura">
                        <div class="label">Temperatura</div>
                        <div class="value" id="temperatura">-- °C</div>
                    </div>
                    <br><br>
                    <a href="/">
                        <button class="boton-regresar"> Regresar al inicio</button>
                    </a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/api/ultimo-dato")
async def api_ultimo_dato():
    return ultimo_dato if ultimo_dato else {"temperatura": 0, "humedad": 0, "timestamp": "Sin datos"}

@app.get("/control_acceso", response_class=HTMLResponse)
async def control_acesso():
    return """
    <html>
        <head><title>Control de acceso</title></head>
        <body>
            <h1>Accesos</h1>
            <h2>No se han recibido datos aún.</h2>
        </body>
    </html>
    """

@app.get("/control_de_dispensador", response_class=HTMLResponse)
async def control_de_dispensador():
    return """
    <html>
        <head>
            <title>Control de dispensadores</title>
            <script>
                async function enviarComando(valor) {
                    await fetch(`/enviar/${valor}`);
                    alert("Comando enviado: " + valor);
                }
            </script>
            <style>
                body {
                    background-image: url('https://i.pinimg.com/originals/ef/68/f2/ef68f211a53b53c952a1445c16dcab6b.jpg');
                    background-size: cover;
                    background-position: center;
                    font-family: 'Arial', sans-serif;
                    color: white;
                    text-align: center;
                }

                .container {
                    background-color: rgba(0, 0, 0, 0.5);
                    border-radius: 20px;
                    padding: 30px;
                    margin: 60px auto;
                    max-width: 700px;
                }

                h2 {
                    font-size: 22px;
                    color: white;
                }
                .seccion {
                    display: inline-block;
                    width: 45%;
                    vertical-align: top;
                    margin: 20px;
                }
                .btn {
                    display: block;
                    margin: 10px auto;
                    padding: 10px 20px;
                    font-size: 16px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    width: 80%;
                }
                .comida {
                    background-color: #3498db;
                    color: white;
                }
                .agua-on {
                    background-color: #a3e635;
                    color: black;
                }
                .agua-off {
                    background-color: #ef4444;
                    color: white;
                }
                .estado {
                    margin-top: 20px;
                    font-weight: bold;
                }
                .volver {
                    background-color: #3498db;
                    color: white;
                    font-size: 16px;
                    padding: 10px 20px;
                    border: none;
                    border-radius: 10px;
                    cursor: pointer;
                    margin-top: 20px;
                }
                .volver:hover {
                    background-color: #2980b9;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="seccion">
                    <h2>Dispensador de comida</h2>
                    <button class="btn comida" onclick="enviarComando('comida1')">Nivel 1</button>
                    <button class="btn comida" onclick="enviarComando('comida2')">Nivel 2</button>
                    <button class="btn comida" onclick="enviarComando('comida3')">Nivel 3</button>
                    <button class="btn comida" onclick="enviarComando('reiniciar')">Reiniciar dispensador</button>
                    <hr>
                </div>

                <div class="seccion">
                    <h2>Control de agua</h2>
                    <button class="btn agua-on" onclick="enviarComando('agua1')">Activar bebedero</button>
                    <button class="btn agua-off" onclick="enviarComando('agua0')">Desactivar bebedero</button>
                    <hr>
                </div>

                <div style="margin-top: 40px;">
                    <a href="/">
                        <button class="volver"> Regresar al inicio</button>
                    </a>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/enviar/{comando}")
async def enviar_comando(comando: str):
    global ultimo_comando
    ultimo_comando = comando
    return {"status": "ok", "comando": comando}


@app.get("/leer-comando")
async def leer_comando():
    global ultimo_comando
    comando = ultimo_comando
    ultimo_comando = ""  # limpia el comando una vez leído
    return {"comando": comando}

# Ejecutar si se corre directamente
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="localhost", port=9090)
