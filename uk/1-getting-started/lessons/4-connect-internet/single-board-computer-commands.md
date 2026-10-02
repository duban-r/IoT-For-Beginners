# Керування нічником через Інтернет: віртуальний IoT-пристрій і Raspberry Pi

У цій частині уроку ви підпишете Raspberry Pi або віртуальний IoT-пристрій на команди, які надходять через MQTT-брокер.

## Підписка на команди

Наступний крок — підписатися на команди від MQTT-брокера й реагувати на них.

### Завдання

Підпишіться на команди.

1. Відкрийте проєкт нічника у VS Code.

1. Переконайтеся, що в терміналі активовано віртуальне середовище.

1. Після оголошення `client_telemetry_topic` додайте:

    ```python
    server_command_topic = id + '/commands'
    ```

    `server_command_topic` — це MQTT-тема, на яку пристрій підпишеться, щоб отримувати команди для світлодіода.

1. Додайте в кінець функції `handle_connect` рядок, який підписує клієнта на тему команд:

    ```python
        client.subscribe(server_command_topic)
    ```

    Підписуватися саме в `handle_connect` зручно: якщо з'єднання обірветься й відновиться, бібліотека знову викличе цю функцію, і підписка відновиться автоматично.

1. Одразу після функції `handle_connect` додайте функцію, яка обробляє команди:

    ```python
    def handle_command(client, userdata, message):
        payload = json.loads(message.payload.decode())
        print('Отримано команду:', payload)

        if payload['led_on']:
            led.on()
        else:
            led.off()
    ```

    Функція `handle_command` читає повідомлення як JSON-документ і перевіряє значення властивості `led_on`. Якщо воно `True`, світлодіод вмикається, інакше вимикається.

1. Після рядка `mqtt_client.on_connect = handle_connect` додайте:

    ```python
    mqtt_client.on_message = handle_command
    ```

    Тепер функція `handle_command` викликатиметься щоразу, коли надходить повідомлення.

    > 💁 Обробник `on_message` викликається для всіх тем, на які підписано клієнта. Якщо згодом ви слухатимете кілька тем, назву теми можна дізнатися з `message.topic`.

    Початок вашого коду після сенсора й світлодіода має виглядати так:

    ```python
    id = '<ID>'

    client_name = id + 'nightlight_client'
    client_telemetry_topic = id + '/telemetry'
    server_command_topic = id + '/commands'


    def handle_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print('Не вдалося підключитися до MQTT:', reason_code)
            return

        print('Підключено до MQTT!')
        client.subscribe(server_command_topic)


    def handle_command(client, userdata, message):
        payload = json.loads(message.payload.decode())
        print('Отримано команду:', payload)

        if payload['led_on']:
            led.on()
        else:
            led.off()


    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
    mqtt_client.on_connect = handle_connect
    mqtt_client.on_message = handle_command
    mqtt_client.connect('test.mosquitto.org')
    mqtt_client.loop_start()
    ```

1. Запустіть код так само, як у попередній частині завдання. Якщо ви використовуєте віртуальний IoT-пристрій, переконайтеся, що застосунок CounterFit запущено, а сенсор освітлення й світлодіод створено на правильних пінах. Серверний код теж має працювати.

1. Змінюйте рівень освітлення для фізичного чи віртуального пристрою. У терміналі з'являтимуться отримані команди, а світлодіод вмикатиметься й вимикатиметься залежно від рівня освітлення:

    ```output
    (.venv) ➜  nightlight python app.py
    Підключено до MQTT!
    Надсилаю телеметрію: {"light": 0}
    Отримано команду: {'led_on': True}
    Надсилаю телеметрію: {"light": 500}
    Отримано команду: {'led_on': False}
    ```

> 💁 Цей код є в папці [code-commands/virtual-device](code-commands/virtual-device) або [code-commands/pi](code-commands/pi).

😀 Ви запрограмували пристрій реагувати на команди з MQTT-брокера.
