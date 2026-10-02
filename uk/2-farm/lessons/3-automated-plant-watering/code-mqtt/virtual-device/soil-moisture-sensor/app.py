import json
import time

import paho.mqtt.client as mqtt
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()
relay = GroveRelay(5)

id = '<ID>'

client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(server_command_topic)


def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Отримано команду:', payload)

    if payload['relay_on']:
        relay.on()
    else:
        relay.off()


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_command
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    soil_moisture = adc.read(0)
    print('Вологість ґрунту:', soil_moisture)

    mqtt_client.publish(client_telemetry_topic, json.dumps({'soil_moisture': soil_moisture}))

    time.sleep(10)
