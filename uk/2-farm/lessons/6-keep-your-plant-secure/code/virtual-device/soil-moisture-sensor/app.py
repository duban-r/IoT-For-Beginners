import json
import time

from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse, X509
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

CounterFitConnection.init('127.0.0.1', 5000)

host_name = '<host_name>.azure-devices.net'
device_id = 'soil-moisture-sensor-x509'
x509 = X509('./soil-moisture-sensor-x509-cert.pem', './soil-moisture-sensor-x509-key.pem')

adc = ADC()
relay = GroveRelay(5)

device_client = IoTHubDeviceClient.create_from_x509_certificate(x509, host_name, device_id)

print('Підключення')
device_client.connect()
print('Підключено')


def handle_method_request(request):
    print('Отримано прямий метод:', request.name)

    if request.name == 'relay_on':
        relay.on()
    elif request.name == 'relay_off':
        relay.off()

    method_response = MethodResponse.create_from_method_request(request, 200)
    device_client.send_method_response(method_response)


device_client.on_method_request_received = handle_method_request

while True:
    soil_moisture = adc.read(0)
    print('Вологість ґрунту:', soil_moisture)

    message = Message(json.dumps({'soil_moisture': soil_moisture}))
    device_client.send_message(message)

    time.sleep(10)
