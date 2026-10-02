import json
import time

import paho.mqtt.client as mqtt

from os import path
import csv
from datetime import datetime

id = '<ID>'

client_name = id + 'temperature_sensor_server'
client_telemetry_topic = id + '/telemetry'


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(client_telemetry_topic)


temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']

if not path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Отримано повідомлення:', payload)

    with open(temperature_file_name, mode='a', newline='') as temperature_file:
        temperature_writer = csv.DictWriter(temperature_file, fieldnames=fieldnames)
        temperature_writer.writerow({'date' : datetime.now().astimezone().replace(microsecond=0).isoformat(), 'temperature' : payload['temperature']})


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    time.sleep(2)
