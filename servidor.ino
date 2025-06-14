#include <DHT.h>
#include <Servo.h>

// sensores
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#define PIN_SENSOR_HUMO A0

// Pines de actuadores
#define PIN_COMIDA_1 2
#define PIN_COMIDA_2 3
#define PIN_COMIDA_3 5
#define PIN_BEBEDERO 6
#define PIN_PUERTA 7
#define PIN_BOCINA 8

Servo servoComida1;
Servo servoComida2;
Servo servoComida3;
Servo Puerta;

int ultimoNivel = 0;
unsigned long ultimoTiempoNivel = 0;
const unsigned long esperaNivel = 1000;

unsigned long tiempoAnterior = 0;
const unsigned long intervalo = 5000;

bool puertaabiertahumo = false;  

void setup() {
  Serial.begin(9600);
  dht.begin();

  servoComida1.attach(PIN_COMIDA_1);
  servoComida2.attach(PIN_COMIDA_2);
  servoComida3.attach(PIN_COMIDA_3);
  Puerta.attach(PIN_PUERTA);

  pinMode(PIN_BEBEDERO, OUTPUT);
  pinMode(PIN_BOCINA, OUTPUT);
  
  pinMode(PIN_SENSOR_HUMO, INPUT);

  // Iniciar todo apagado
  servoComida1.write(180);
  servoComida2.write(180);
  servoComida3.write(180);
  Puerta.write(0);

  digitalWrite(PIN_BEBEDERO, LOW);
  digitalWrite(PIN_BOCINA, LOW);

}

void loop() {
  // 1. Enviar temperatura y humedad cada 5s
  if (millis() - tiempoAnterior >= intervalo) {
    tiempoAnterior = millis();
    float h = dht.readHumidity();
    float t = dht.readTemperature();
    if (!isnan(h) && !isnan(t)) {
      Serial.print("T:");
      Serial.print(t);
      Serial.print(",H:");
      Serial.println(h);
    }
  }

  // 2. Leer comandos del servidor
  if (Serial.available()) {
    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando == "comida1") {
       servoComida1.write(90);
    } else if (comando == "comida2") {
        servoComida2.write(90);
    } else if (comando == "comida3") {
        servoComida3.write(90);
    } else if (comando == "reiniciar") {
      servoComida1.write(180);
      servoComida2.write(180);
      servoComida3.write(180);
    } else if (comando == "agua1") {
      digitalWrite(PIN_BEBEDERO, HIGH);
    } else if (comando == "agua0") {
      digitalWrite(PIN_BEBEDERO, LOW);
    } else if (comando == "puerta_abierta") {
      Puerta.write(90); 
    } else if (comando == "puerta_cerrada") {
      Puerta.write(0);
      puertaabiertahumo = false;
    }

    Serial.println("Comando ejecutado: " + comando);
  }

  // 3. Monitorear sensor de humo
  int valorHumo = analogRead(PIN_SENSOR_HUMO); 
  
  if (valorHumo > 500 && !puertaabiertahumo) { 
    Puerta.write(90);
    Serial.println("Alerta: Humo detectado, puerta abierta.");
    puertaabiertahumo = true;
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
    digitalWrite(PIN_BOCINA, HIGH);
    delay(150);
    digitalWrite(PIN_BOCINA, LOW);
    delay(150);
  } 
  }