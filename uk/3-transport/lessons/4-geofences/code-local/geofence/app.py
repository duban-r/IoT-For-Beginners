import json
import math
import time

import paho.mqtt.client as mqtt
from shapely.affinity import scale
from shapely.geometry import Point, shape

id = '<ID>'

client_name = id + 'geofence_server'
client_telemetry_topic = id + '/telemetry'

search_buffer = 50

with open('geofence.json') as file:
    geofence = shape(json.load(file)['features'][0]['geometry'])


def to_meters(geometry, lat):
    return scale(geometry, xfact=111_320 * math.cos(math.radians(lat)), yfact=110_540, origin=(0, 0))


def check_geofence(lat, lon):
    point = Point(lon, lat)
    distance = to_meters(geofence.exterior, lat).distance(to_meters(point, lat))

    if geofence.contains(point):
        distance = -distance

    if distance > search_buffer:
        print('Точка поза геозоною')
    elif distance > 0:
        print(f'Точка трохи поза геозоною, на відстані {distance:.0f} м')
    elif distance < -search_buffer:
        print('Точка всередині геозони')
    else:
        print(f'Точка трохи всередині геозони, на відстані {-distance:.0f} м від межі')


def handle_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print('Не вдалося підключитися до MQTT:', reason_code)
        return

    print('Підключено до MQTT!')
    client.subscribe(client_telemetry_topic)


def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print('Отримано повідомлення:', payload)
    check_geofence(payload['gps']['lat'], payload['gps']['lon'])


mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
mqtt_client.on_connect = handle_connect
mqtt_client.on_message = handle_telemetry
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

while True:
    time.sleep(2)
