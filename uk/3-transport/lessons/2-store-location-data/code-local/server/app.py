import csv
import json
import os
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

id = '<ID>'

client_name = id + 'gps_server'
client_telemetry_topic = id + '/telemetry'

data_file = 'gps_data.csv'


def save_gps_data(gps):
    timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    new_file = not os.path.exists(data_file)

    with open(data_file, 'a', newline='') as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(['timestamp', 'lat', 'lon'])
        writer.writerow([timestamp, gps['lat'], gps['lon']])

    print('Записано рядок:', timestamp, gps['lat'], gps['lon'])


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Отримано повідомлення:', payload)
    save_gps_data(payload['gps'])


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    time.sleep(2)
