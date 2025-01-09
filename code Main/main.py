import machine
import time
import camera
import base64
from umqtt.simple import MQTTClient
from machine import Pin, deepsleep, RTC
import esp32

# Configuration MQTT
BROKER_IP = "192.168.1.179"
BROKER_PORT = 1883
TOPIC1 = "esp32/camera/photo"
TOPIC2 = "esp32/battery"

# GPIO pour le capteur PIR et la mesure de batterie
PIR_PIN = 13
BATTERY_LEVEL = 75  # Exemple : niveau de la batterie en pourcentage
LED_PIN = 4

# Initialisation des capteurs
pir_sensor = Pin(PIR_PIN, Pin.IN)
led = Pin(LED_PIN, mode=Pin.OUT)
led.value(0)

# Utiliser RTC pour le timestamp
rtc = RTC()

# Enregistrement de l'heure du dernier envoi
last_sent_hour = None

# Fonction pour envoyer une image via MQTT
def send_image_via_mqtt():
    try:
        camera.init(0, format=camera.JPEG)
        img = camera.capture()
        img_base64 = base64.b64encode(img).decode('utf-8')

        client = MQTTClient("esp32_client", BROKER_IP, port=BROKER_PORT)
        client.connect()
        client.publish(TOPIC1, img_base64)
        client.publish(TOPIC2, str(BATTERY_LEVEL))  # Envoyer le niveau de la batterie
        client.disconnect()
        print("Image et niveau de batterie envoyés.")
    except Exception as e:
        print(f"Erreur lors de l'envoi MQTT : {e}")
   

# Vérifier si 24 heures se sont écoulées depuis le dernier envoi
def check_daily_send():
    global last_sent_hour
    current_time = rtc.datetime()  # Obtenir la date et l'heure actuelles
    current_hour = current_time[4]  # Heure actuelle (index 4)

    # Si aucune heure précédente n'est enregistrée ou si 24 heures se sont écoulées
    if last_sent_hour is None or (current_hour - last_sent_hour) % 24 == 0:
        last_sent_hour = current_hour  # Mettre à jour l'heure du dernier envoi
        return True
    return False

# Fonction principale
def main():
    global last_sent_hour

    # Vérifie la raison du réveil
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("Réveillé par le capteur PIR.")
        led.value(1)
        send_image_via_mqtt()
        time.sleep(10)  # Attendre un peu avant de retourner en veille
        led.value(0)
    else:
        # Vérifier si 24 heures se sont écoulées depuis le dernier envoi
        if check_daily_send():
            print("Envoi du niveau de la batterie (1 fois par jour).")
            client = MQTTClient("esp32_client", BROKER_IP, port=BROKER_PORT)
            client.connect()
            client.publish(TOPIC2, str(BATTERY_LEVEL))  # Envoyer uniquement le niveau de la batterie
            client.disconnect()
            print("Envoi du niveau de batterie terminé.")
        else:
            print("Pas encore 24 heures écoulées depuis le dernier envoi.")

    # Configurer le réveil sur interruption externe (capteur PIR)
    esp32.wake_on_ext1(pins=(pir_sensor,), level=esp32.WAKEUP_ALL_LOW)

    # Activer le mode veille profonde
    print("Passage en mode Deep Sleep...")
    deepsleep()

# Lancer la fonction principale
main()

