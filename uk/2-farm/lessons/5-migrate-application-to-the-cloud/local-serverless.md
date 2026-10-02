# Локальний варіант: «безсерверна» функція на вашому комп'ютері

У цій частині уроку ви не створюватимете ресурсів в Azure. Натомість ви напишете ту саму логіку, що й тригер Azure Functions, у вигляді звичайної функції Python і запустите її на своєму комп'ютері. Викликатиме цю функцію невеликий підписник MQTT — він виконуватиме роль середовища виконання Azure Functions.

| Azure Functions (демо викладача) | Локальний варіант |
| --- | --- |
| Тригер `iot_hub_trigger` викликається для кожного повідомлення в IoT Hub | Функція `soil_moisture_trigger` викликається для кожного повідомлення в темі `<ID>/telemetry` |
| Середовище виконання Functions підключається до IoT Hub і викликає функцію | Підписник MQTT підключається до брокера й викликає функцію |
| Функція надсилає запит прямого методу `relay_on` або `relay_off` | Функція повертає команду `{"relay_on": true}` або `{"relay_on": false}`, і її публікують у тему `<ID>/commands` |

Як і безсерверна функція, `soil_moisture_trigger` нічого не пам'ятає між викликами: вона отримує одне повідомлення й повертає одну команду.

## Підготовка

Вам знадобиться IoT-пристрій з [уроку 3](../3-automated-plant-watering/README.md), який надсилає вологість ґрунту через MQTT і вмикає реле за командами. Якщо ви його не зберегли, візьміть готовий код з папки [code-mqtt/virtual-device](../3-automated-plant-watering/code-mqtt/virtual-device) уроку 3 і замініть `<ID>` на свій унікальний ідентифікатор.

## Напишіть «безсерверну» функцію

### Завдання: створіть застосунок

1. Створіть папку `soil-moisture-trigger` і відкрийте її у VS Code.

1. Створіть і активуйте віртуальне середовище Python так само, як для серверного коду в [уроці 4 першого розділу](../../../1-getting-started/lessons/4-connect-internet/README.md#налаштуйте-віртуальне-середовище-python).

1. Встановіть пакет pip для MQTT:

    ```sh
    pip install "paho-mqtt>=2.1"
    ```

1. Створіть файл `app.py` і додайте в нього такий код:

    ```python
    import json
    import time

    import paho.mqtt.client as mqtt

    id = '<ID>'

    client_name = id + 'soilmoisturesensor_trigger'
    client_telemetry_topic = id + '/telemetry'
    server_command_topic = id + '/commands'
    ```

    Замініть `<ID>` на той самий унікальний ідентифікатор, що й у коді пристрою.

1. Під цим кодом додайте саму «безсерверну» функцію:

    ```python
    # "Безсерверна" функція: її викликають для кожного повідомлення телеметрії.
    # Вона нічого не пам'ятає між викликами й лише повертає команду для пристрою.
    def soil_moisture_trigger(body):
        soil_moisture = body['soil_moisture']

        if soil_moisture > 450:
            return {'relay_on': True}
        else:
            return {'relay_on': False}
    ```

    Порівняйте її з кодом функції `iot_hub_trigger` з уроку: вона так само отримує вологість ґрунту з тіла повідомлення й порівнює її з 450. Різниця лише в тому, що замість прямого методу вона повертає команду.

1. Під функцією додайте код, який замінює середовище виконання Azure Functions:

    ```python
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
    ```

    Функція `handle_telemetry` викликається для кожного повідомлення телеметрії. Вона розбирає JSON, викликає `soil_moisture_trigger` і публікує повернуту команду в тему команд пристрою.

### Завдання: запустіть функцію

1. Переконайтеся, що застосунок CounterFit запущено, а сенсор вологості ґрунту й реле створено на пінах 0 і 5, як в уроці 3.

1. Запустіть код пристрою з уроку 3.

1. Запустіть «безсерверну» функцію:

    ```sh
    python app.py
    ```

1. Змінюйте в CounterFit значення вологості ґрунту. Коли воно більше за 450, функція надсилає команду ввімкнути реле, а коли менше — вимкнути:

    ```output
    (.venv) ➜  soil-moisture-trigger python app.py
    Підключено до MQTT!
    Отримано повідомлення: {'soil_moisture': 600}
    Надсилаю команду: {'relay_on': True}
    Отримано повідомлення: {'soil_moisture': 300}
    Надсилаю команду: {'relay_on': False}
    ```

    У терміналі пристрою з'являтимуться отримані команди, а реле в CounterFit вмикатиметься й вимикатиметься:

    ```output
    (.venv) ➜  soil-moisture-sensor python app.py
    Підключено до MQTT!
    Вологість ґрунту: 600
    Отримано команду: {'relay_on': True}
    Вологість ґрунту: 300
    Отримано команду: {'relay_on': False}
    ```

> 💁 Цей код є в папці [code-local/soil-moisture-trigger](code-local/soil-moisture-trigger).

😀 Ви запустили «безсерверну» логіку керування поливом на своєму комп'ютері!
