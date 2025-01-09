import base64
from influxdb_client_3 import InfluxDBClient3, Point
from datetime import datetime

# Configuration
token = "GlSE8Kl0b7L0-wAd68wSKx6MzmZ8UmXRzF2l4tA5qDWF2ORITKD-HRVcn_VOBl7D4LYpPscVMajWxMxBRXQz8A=="  # Votre token InfluxDB Cloud
org = "liege seraing"  # Votre organisation
bucket = "image"  # Nom du bucket
host = "https://us-east-1-1.aws.cloud2.influxdata.com"

# Initialiser le client
client = InfluxDBClient3(host=host, token=token, org=org)

# Encoder l'image en Base64
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"L'image '{image_path}' est introuvable.")
        return None

# Envoyer l'image à InfluxDB
image_path = "image3.jpg"  # Remplacez par le chemin correct de votre image
image_base64 = encode_image_to_base64(image_path)

if image_base64:
    # Créer un point de données avec un timestamp valide
    point = Point("business_media") \
        .tag("type", "image") \
        .field("content", image_base64) \
        .time(datetime.utcnow())  # Utilisation du timestamp actuel avec datetime

    try:
        # Écrire dans InfluxDB (en utilisant "database" pour spécifier le bucket)
        client.write(record=point, database=bucket)  # Utilisez "database" pour le bucket
        print("Image encodée et envoyée à InfluxDB Cloud avec succès.")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans InfluxDB : {e}")

