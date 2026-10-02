import json
import time

import paho.mqtt.client as mqtt
from grove.grove_led import GroveLed
from grove.grove_light_sensor_v1_2 import GroveLightSensor

light_sensor = GroveLightSensor(0)
led = GroveLed(5)

id = '<ID>'

client_name = id + 'nightlight_client'
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

    if payload['led_on']:
        led.on()
    else:
        led.off()


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_command
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    light = light_sensor.light
    telemetry = json.dumps({'light': light})

    print('Надсилаю телеметрію:', telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)
