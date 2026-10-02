import json
import threading
import time

import paho.mqtt.client as mqtt

id = '<ID>'

client_name = id + 'soilmoisturesensor_server'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(client_telemetry_topic)


water_time = 5
wait_time = 20


def send_relay_command(client, state):
    command = {'relay_on': state}
    print('Надсилаю команду:', command)
    client.publish(server_command_topic, json.dumps(command))


def control_relay(client):
    print('Відписуюся від телеметрії')
    client.unsubscribe(client_telemetry_topic)

    send_relay_command(client, True)
    time.sleep(water_time)
    send_relay_command(client, False)

    time.sleep(wait_time)

    print('Знову підписуюся на телеметрію')
    client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Отримано повідомлення:', payload)

    if payload['soil_moisture'] > 450:
        threading.Thread(target=control_relay, args=(client,)).start()


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    time.sleep(2)
