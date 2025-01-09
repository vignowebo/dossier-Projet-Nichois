#This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import time

# Configuration Wi-Fi
SSID = "Omada 1"
PASSWORD = "Valo9550"

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connexion au Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)

    print("Connecté au Wi-Fi avec l'adresse IP :", wlan.ifconfig()[0])

# Connecter au Wi-Fi au démarrage
connect_wifi()

