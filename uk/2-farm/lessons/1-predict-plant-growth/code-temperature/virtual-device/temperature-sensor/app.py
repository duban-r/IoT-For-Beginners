import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT

CounterFitConnection.init('127.0.0.1', 5000)

sensor = DHT('11', 5)

while True:
    _, temp = sensor.read()
    print(f'Температура {temp}°C')

    time.sleep(10)
