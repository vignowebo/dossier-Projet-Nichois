from machine import Pin
import time

# Configurer le bouton sur le GPIO 3
button = Pin(13, Pin.IN, Pin.PULL_UP)  # Bouton en mode Pull-up (le bouton est connecté à GND)

# Configurer la LED intégrée (sur GPIO 4 de l'ESP32-Cam)
led = Pin(4, Pin.OUT)  # La LED est connectée au GPIO 4

# Fonction principale pour tester le bouton et contrôler la LED
def main():
    print("Appuyez sur le bouton pour faire clignoter la LED")
    
    while True:
        if button.value() == 0:  # Si le bouton est pressé (niveau bas)
            print("Bouton pressé! La LED clignote...")
            led.value(1)  # Allumer la LED
            time.sleep(0.5)  # Attendre 0.5 seconde
            led.value(0)  # Éteindre la LED
            time.sleep(0.5)  # Attendre 0.5 seconde
        else:
            led.value(0)  # Si le bouton n'est pas pressé, la LED reste éteinte

        time.sleep(0.1)  # Petite pause pour éviter une boucle trop rapide

# Lancer la fonction principale
main()

