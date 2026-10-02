import json
import logging
import math
import os
import uuid

import azure.functions as func
from azure.storage.blob import BlobServiceClient, PublicAccess
from shapely.affinity import scale
from shapely.geometry import Point, shape

app = func.FunctionApp()


def get_or_create_container(name):
    connection_str = os.environ['STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)

    for container in blob_service_client.list_containers():
        if container.name == name:
            return blob_service_client.get_container_client(container.name)

    return blob_service_client.create_container(name, public_access=PublicAccess.Container)


@app.event_hub_message_trigger(arg_name='events',
                               event_hub_name='samples-workitems',
                               connection='IOT_HUB_CONNECTION_STRING',
                               cardinality=func.Cardinality.MANY,
                               consumer_group='$Default')
def iot_hub_trigger(events: list[func.EventHubEvent]):
    for event in events:
        logging.info('Отримано подію з IoT Hub: %s',
                     event.get_body().decode('utf-8'))

        device_id = event.iothub_metadata['connection-device-id']
        blob_name = f'{device_id}/{str(uuid.uuid1())}.json'

        container_client = get_or_create_container('gps-data')
        blob = container_client.get_blob_client(blob_name)

        event_body = json.loads(event.get_body().decode('utf-8'))
        blob_body = {
            'device_id': device_id,
            'timestamp': event.iothub_metadata['enqueuedtime'],
            'gps': event_body['gps']
        }

        logging.info(f'Записую blob {blob_name}: {blob_body}')
        blob.upload_blob(json.dumps(blob_body).encode('utf-8'))


search_buffer = 50

with open(os.path.join(os.path.dirname(__file__), 'geofence.json')) as file:
    geofence = shape(json.load(file)['features'][0]['geometry'])


def to_meters(geometry, lat):
    return scale(geometry, xfact=111_320 * math.cos(math.radians(lat)), yfact=110_540, origin=(0, 0))


@app.event_hub_message_trigger(arg_name='events',
                               event_hub_name='samples-workitems',
                               connection='IOT_HUB_CONNECTION_STRING',
                               cardinality=func.Cardinality.MANY,
                               consumer_group='geofence')
def geofence_trigger(events: list[func.EventHubEvent]):
    for event in events:
        event_body = json.loads(event.get_body().decode('utf-8'))
        lat = event_body['gps']['lat']
        lon = event_body['gps']['lon']

        point = Point(lon, lat)
        distance = to_meters(geofence.exterior, lat).distance(to_meters(point, lat))

        if geofence.contains(point):
            distance = -distance

        if distance > search_buffer:
            logging.info('Точка поза геозоною')
        elif distance > 0:
            logging.info(f'Точка трохи поза геозоною, на відстані {distance:.0f} м')
        elif distance < -search_buffer:
            logging.info('Точка всередині геозони')
        else:
            logging.info(f'Точка трохи всередині геозони, на відстані {-distance:.0f} м від межі')
