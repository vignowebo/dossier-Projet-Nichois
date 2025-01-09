from machine import Pin, deepsleep
import esp32
import time
import machine

# Définir les GPIO
BUTTON_PIN = 13  # GPIO du bouton poussoir
LED_PIN = 4      # GPIO de la LED

# Configurer le bouton en entrée avec pull-up
button = Pin(BUTTON_PIN, mode=Pin.IN, pull=Pin.PULL_UP)

# Configurer la LED en sortie
led = Pin(LED_PIN, mode=Pin.OUT)
led.value(0)  # Assurez-vous que la LED est éteinte au départ

# Vérifier la cause du réveil
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("Réveil depuis le mode Deep Sleep")
    # Allumer la LED pendant 30 secondes
    led.value(1)
    print("LED allumée pendant 5 secondes...")
    time.sleep(5)
    led.value(0)
    print("LED éteinte, retour en mode Deep Sleep")

# Configurer le bouton comme source de réveil
# Utiliser wake_on_ext1 pour configurer plusieurs GPIO comme source de réveil
esp32.wake_on_ext1(pins=(button,), level=esp32.WAKEUP_ALL_LOW)

# Entrer en mode Deep Sleep
print("Passage en mode Deep Sleep...")
deepsleep()

