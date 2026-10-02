import json
import time

import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT

CounterFitConnection.init('127.0.0.1', 5000)

sensor = DHT('11', 5)

id = '<ID>'

client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    _, temp = sensor.read()
    telemetry = json.dumps({'temperature': temp})

    print('Надсилаю телеметрію:', telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10 * 60)
