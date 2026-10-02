import json
import logging
import os

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

app = func.FunctionApp()


@app.function_name(name='iot-hub-trigger')
@app.event_hub_message_trigger(arg_name='event',
                               event_hub_name='',
                               connection='IOT_HUB_CONNECTION_STRING',
                               cardinality=func.Cardinality.ONE)
def iot_hub_trigger(event: func.EventHubEvent):
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Отримано повідомлення: {body} від {device_id}')

    soil_moisture = body['soil_moisture']

    if soil_moisture > 450:
        direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
    else:
        direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')

    logging.info(f'Надсилаю запит прямого методу {direct_method.method_name} на пристрій {device_id}')

    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager.from_connection_string(registry_manager_connection_string)

    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Запит прямого методу надіслано!')
