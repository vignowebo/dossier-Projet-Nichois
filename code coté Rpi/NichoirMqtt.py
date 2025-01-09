from datetime import datetime
import base64
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient, Point

# InfluxDB Cloud settings
INFLUXDB_URL = "https://us-east-1-1.aws.cloud2.influxdata.com/"
INFLUXDB_TOKEN = "yK9CfaxcEK9nfCcpgPqxomZm6BrjXl8HjZG3fkEyTv2jB-uEubYSNctlVUycg_oa62pVgqYgmNVCuAdOUd6aeg=="
INFLUXDB_ORG = "liege seraing"
BUCKET_IMAGE = "IMAGE"
BUCKET_BATTERY = "BATTERY"

# MQTT settings
BROKER_IP = "192.168.1.179"
PORT = 1883
TOPIC_PHOTO = "esp32/camera/photo"
TOPIC_BAT = "esp32/battery"

# Initialiser le client InfluxDB
influx_client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)
write_api = influx_client.write_api()

# Callback lors de la connexion MQTT
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC_PHOTO)
    client.subscribe(TOPIC_BAT)

# Callback lors de la réception de messages MQTT
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        if msg.topic == TOPIC_PHOTO:
            image_base64 = msg.payload.decode('utf-8')
            point = Point("camera_data") \
                .tag("type", "image") \
                .field("content", image_base64) \
                .time(datetime.utcnow())
            write_api.write(bucket=BUCKET_IMAGE, record=point)
            print("Image data sent to InfluxDB.")
        elif msg.topic == TOPIC_BAT:
            bat_status = int(msg.payload.decode('utf-8'))
            point = Point("bat_data") \
                .tag("sensor", "bat") \
                .field("status", bat_status) \
                .time(datetime.utcnow())
            write_api.write(bucket=BUCKET_BATTERY, record=point)
            print(f"BATTERY status sent to InfluxDB: {bat_status}")
    except Exception as e:
        print(f"Error processing message from topic {msg.topic}: {e}")

# Configurer le client MQTT
mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connexion au broker MQTT
mqtt_client.connect(BROKER_IP, PORT, 60)

# Lancer la boucle MQTT
try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
    mqtt_client.disconnect()
