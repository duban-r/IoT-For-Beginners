import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay

CounterFitConnection.init('127.0.0.1', 5000)

adc = ADC()
relay = GroveRelay(5)

while True:
    soil_moisture = adc.read(0)
    print('Вологість ґрунту:', soil_moisture)

    if soil_moisture > 450:
        print('Вологість ґрунту замала, вмикаю реле.')
        relay.on()
    else:
        print('Вологість ґрунту в нормі, вимикаю реле.')
        relay.off()

    time.sleep(10)
