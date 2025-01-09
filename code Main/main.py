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

# GPIO pour le capteur PIR et la LED
PIR_PIN = 13
LED_PIN = 4

# Initialisation des capteurs
pir_sensor = Pin(PIR_PIN, Pin.IN)
led = Pin(LED_PIN, mode=Pin.OUT)
led.value(0)

# Utiliser RTC pour le timestamp
rtc = RTC()
last_sent_hour = None
BATTERY_LEVEL = 75  # Exemple : niveau de la batterie en pourcentage

# Fonction pour configurer la caméra
def config_camera(resolution="SVGA", quality=10):
    resolution_map = {
        "QQVGA": 0,  # 160x120
        "QVGA": 1,   # 320x240
        "VGA": 2,    # 640x480
        "SVGA": 3,   # 800x600
        "XGA": 4,    # 1024x768
        "UXGA": 5    # 1600x1200
    }

    try:
        if resolution not in resolution_map:
            print(f"Résolution inconnue : {resolution}. Réglage par défaut à QVGA.")
            resolution = "QVGA"

        camera.framesize(resolution_map[resolution])
        camera.quality(quality)
        print(f"Caméra configurée : Résolution = {resolution}, Qualité = {quality}")
    except Exception as e:
        print(f"Erreur lors de la configuration de la caméra : {e}")

# Fonction pour capturer une image
def capture_image():
    try:
        led.value(1)  # Allumer la LED pour capturer l'image
        time.sleep(0.5)
        img = camera.capture()
        led.value(0)  # Éteindre la LED
        if img:
            print(f"Image capturée avec succès, taille : {len(img)} octets.")
            return img
        else:
            raise ValueError("Erreur : échec de la capture de l'image.")
    except Exception as e:
        print(f"Erreur lors de la capture : {e}")
        return None

# Fonction pour envoyer une image via MQTT
def send_image_via_mqtt():
    try:
        if not camera.init():
            print("Erreur : Impossible d'initialiser la caméra.")
            return

        config_camera(resolution="SVGA", quality=10)
        img = capture_image()
        if img:
            img_base64 = base64.b64encode(img).decode('utf-8')

            client = MQTTClient("esp32_client", BROKER_IP, port=BROKER_PORT)
            client.connect()
            client.publish(TOPIC1, img_base64)
            client.publish(TOPIC2, str(BATTERY_LEVEL))  # Envoyer le niveau de la batterie
            client.disconnect()
            print("Image et niveau de batterie envoyés.")
        else:
            print("Aucune image capturée.")
    except Exception as e:
        print(f"Erreur lors de l'envoi MQTT : {e}")
    finally:
        try:
            camera.deinit()
        except Exception as e:
            print(f"Erreur lors de la désinitialisation de la caméra : {e}")

# Fonction principale
def main():
    if machine.reset_cause() == machine.DEEPSLEEP_RESET:
        print("Réveillé par le capteur PIR.")
        send_image_via_mqtt()

    # Configurer le réveil sur interruption externe (capteur PIR)
    esp32.wake_on_ext1(pins=(pir_sensor,), level=esp32.WAKEUP_ALL_LOW)

    # Activer le mode veille profonde
    print("Passage en mode Deep Sleep...")
    deepsleep()

if __name__ == "__main__":
    main()
