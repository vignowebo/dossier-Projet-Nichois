import camera
import network
import time
import base64
from umqtt.simple import MQTTClient
from machine import Pin

# Configurer votre réseau Wi-Fi et MQTT
SSID = "Omada 1"
PASSWORD = "Valo9550"
BROKER_IP = "192.168.1.179"  # Adresse IP de votre broker MQTT
BROKER_PORT = 1883
TOPIC = "esp32/camera/photo"

# GPIO 3 pour le bouton
BUTTON_PIN = 13

# Connexion Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(SSID, PASSWORD)

# Attendre la connexion Wi-Fi
while not wifi.isconnected():
    time.sleep(1)

print("Connecté au Wi-Fi avec l'adresse IP", wifi.ifconfig()[0])

# Configurer le bouton (GPIO 3) pour détecter un appui
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)  # Le bouton est en pull-up (il est connecté à GND)

# Fonction pour envoyer une image en base64 via MQTT
def send_image_via_mqtt():
    # Initialisation de la caméra
    camera.init()
    
    # Capture de l'image
    img = camera.capture()

    # Encoder l'image en base64
    img_base64 = base64.b64encode(img).decode('utf-8')  # Convertir l'image en base64 et en chaîne UTF-8

    # Connexion au broker MQTT
    client = MQTTClient("esp32_client", BROKER_IP, port=BROKER_PORT)
    client.connect()

    # Publier l'image encodée en base64 sur le topic MQTT
    client.publish(TOPIC, img_base64)

    # Déconnexion du broker
    client.disconnect()

# Fonction principale pour détecter l'appui sur le bouton et envoyer l'image
def main():
    print("Appuyez sur le bouton pour capturer et envoyer l'image via MQTT")

    while True:
        if button.value() == 0:  # Le bouton est pressé (GND -> LOW)
            print("Bouton pressé! Capture de l'image et envoi via MQTT...")
            send_image_via_mqtt()
            time.sleep(5)  # Délai de 5 secondes pour éviter les pressions multiples rapides

        time.sleep(0.1)  # Petite pause pour ne pas trop solliciter le processeur

# Lancer la fonction principale
main()

