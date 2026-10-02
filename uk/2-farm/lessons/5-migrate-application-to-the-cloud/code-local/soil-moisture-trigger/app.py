import json
import time

import paho.mqtt.client as mqtt

id = '<ID>'

client_name = id + 'soilmoisturesensor_trigger'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'


# "Безсерверна" функція: її викликають для кожного повідомлення телеметрії.
# Вона нічого не пам'ятає між викликами й лише повертає команду для пристрою.
def soil_moisture_trigger(body):
    soil_moisture = body['soil_moisture']

    if soil_moisture > 450:
        return {'relay_on': True}
    else:
        return {'relay_on': False}


# Далі код, який у хмарі замінює середовище виконання Azure Functions:
# він отримує подію (повідомлення MQTT), викликає функцію й надсилає команду.
def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    body = json.loads(message.payload.decode())
    print('Отримано повідомлення:', body)

    command = soil_moisture_trigger(body)
    print('Надсилаю команду:', command)

    client.publish(server_command_topic, json.dumps(command))


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    time.sleep(2)
