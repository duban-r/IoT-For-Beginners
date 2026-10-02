from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import json
import time

import counterfit_shims_serial
import paho.mqtt.client as mqtt
import pynmea2

id = '<ID>'

client_name = id + 'gps_sensor_client'
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

serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')


def send_gps_data(line):
    msg = pynmea2.parse(line)
    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1

        if msg.lon_dir == 'W':
            lon = lon * -1

        telemetry = json.dumps({'gps': {'lat': lat, 'lon': lon}})
        print('Надсилаю телеметрію:', telemetry)
        mqtt_client.publish(client_telemetry_topic, telemetry)


while True:
    line = serial.readline().decode('utf-8')

    while len(line) > 0:
        send_gps_data(line)
        line = serial.readline().decode('utf-8')

    time.sleep(5)
