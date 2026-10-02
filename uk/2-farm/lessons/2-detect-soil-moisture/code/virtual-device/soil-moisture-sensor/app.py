import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC

CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()

while True:
    soil_moisture = adc.read(0)
    print('Вологість ґрунту:', soil_moisture)

    time.sleep(10)
