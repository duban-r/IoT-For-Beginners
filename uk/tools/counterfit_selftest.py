"""Перевірка CounterFit: створює всі віртуальні сенсори й актуатори курсу та читає їх через шими.

Запуск (з активованим віртуальним середовищем, у якому встановлено CounterFit і шими):
    1. В одному терміналі: counterfit
    2. В іншому:           python counterfit_selftest.py

Скрипт додає сенсори в запущений CounterFit, тож запускайте його на «чистому» CounterFit,
а не під час заняття.
"""
import base64
import io

import requests
from PIL import Image

BASE = 'http://127.0.0.1:5000/'


def post(path, data):
    response = requests.post(BASE + path, json=data, timeout=10)
    response.raise_for_status()


def create_everything():
    image = io.BytesIO()
    Image.new('RGB', (800, 600), (200, 30, 30)).save(image, 'JPEG')

    post('create_sensor', {'type': 'Light', 'pin': 0, 'unit': 'NoUnits'})
    post('create_sensor', {'type': 'Soil Moisture', 'pin': 1, 'unit': 'NoUnits'})
    post('create_sensor', {'type': 'Humidity', 'pin': 5, 'unit': 'Percent'})
    post('create_sensor', {'type': 'Temperature', 'pin': 6, 'unit': 'Celsius'})
    post('create_sensor', {'type': 'UART GPS', 'port': '/dev/ttyAMA0'})
    post('create_sensor', {'type': 'Camera', 'name': 'Picamera'})
    post('create_sensor', {'type': 'Distance', 'i2c_pin': 0x29, 'i2c_unit': 'Millimeter'})
    post('create_actuator', {'type': 'LED', 'port': '5'})
    post('create_actuator', {'type': 'Relay', 'port': '2'})

    post('integer_sensor_settings', {'port': '0', 'value': 250, 'is_random': False, 'random_min': 0, 'random_max': 1023})
    post('integer_sensor_settings', {'port': '1', 'value': 450, 'is_random': False, 'random_min': 0, 'random_max': 1023})
    post('float_sensor_settings', {'port': '5', 'value': 55.5, 'is_random': False, 'random_min': 0, 'random_max': 100})
    post('float_sensor_settings', {'port': '6', 'value': 21.5, 'is_random': False, 'random_min': 0, 'random_max': 40})
    post('gps_sensor_settings', {'port': '/dev/ttyAMA0', 'repeat': True, 'source': 'latlon',
                                 'lat': 50.45, 'lon': 30.52, 'number_of_satellites': 5})
    post('camera_sensor_settings', {'port': 'Picamera', 'source': 'File', 'image_file_name': 'test.jpg',
                                    'file_contents': base64.b64encode(image.getvalue()).decode()})
    post('integer_sensor_settings', {'port': '41', 'value': 120, 'is_random': False, 'random_min': 0, 'random_max': 2000})


def check(name, func, expected):
    try:
        value = func()
        status = 'OK' if value == expected else f'НЕОЧІКУВАНО (очікувалось {expected})'
    except Exception as error:  # noqa: BLE001 - показуємо будь-яку помилку
        value, status = '-', f'ПОМИЛКА: {error}'
    print(f'{name:28} {value!s:24} {status}')
    return status == 'OK'


def main():
    create_everything()

    from counterfit_connection import CounterFitConnection
    CounterFitConnection.init('127.0.0.1', 5000)

    from counterfit_shims_grove.adc import ADC
    from counterfit_shims_grove.grove_led import GroveLed
    from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
    from counterfit_shims_grove.grove_relay import GroveRelay

    def led():
        led = GroveLed(5)
        led.on()
        led.off()
        return 'on/off'

    def relay():
        relay = GroveRelay(2)
        relay.on()
        relay.off()
        return 'on/off'

    def dht():
        from counterfit_shims_seeed_python_dht import DHT
        return DHT('11', 5).read()

    def gps():
        import counterfit_shims_serial
        import pynmea2
        line = counterfit_shims_serial.Serial('/dev/ttyAMA0').readline().decode('utf-8').strip()
        message = pynmea2.parse(line)
        return (round(message.latitude, 2), round(message.longitude, 2))

    def camera():
        from counterfit_shims_picamera import PiCamera
        camera = PiCamera()
        camera.resolution = (640, 480)
        image = io.BytesIO()
        camera.capture(image, 'jpeg')
        image.seek(0)
        return Image.open(image).size

    def distance():
        from counterfit_shims_rpi_vl53l0x.vl53l0x import VL53L0X
        sensor = VL53L0X()
        sensor.begin()
        sensor.wait_ready()
        return sensor.get_distance()

    results = [
        check('Світло (GroveLightSensor)', lambda: GroveLightSensor(0).light, 250),
        check('Світлодіод (GroveLed)', led, 'on/off'),
        check('Вологість ґрунту (ADC)', lambda: ADC().read(1), 450),
        check('Реле (GroveRelay)', relay, 'on/off'),
        check('Температура й вологість', dht, (55.5, 21.5)),
        check('GPS (serial)', gps, (50.45, 30.52)),
        check('Камера (PiCamera)', camera, (640, 480)),
        check('Відстань (VL53L0X)', distance, 120),
    ]
    print()
    print('Усе працює.' if all(results) else 'Є проблеми, див. рядки вище.')


if __name__ == '__main__':
    main()
