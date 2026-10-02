# Зберігання GPS-даних: локальний варіант (MQTT і CSV)

У цій частині уроку ви зробите те саме, що викладач показує в Azure, але на своєму комп'ютері й без облікового запису Azure:

| Azure (демо викладача) | Локальний варіант |
| --- | --- |
| Пристрій надсилає GPS-дані в IoT Hub | Пристрій надсилає GPS-дані через MQTT-брокер `test.mosquitto.org` |
| Azure Functions отримує кожну подію | Python-сервер підписується на MQTT-тему й отримує кожне повідомлення |
| Функція записує кожну точку як JSON-блоб у blob-сховище | Сервер дописує кожну точку рядком у CSV-файл `gps_data.csv` |

CSV (comma-separated values) — це простий текстовий формат таблиць: кожен рядок файлу — рядок таблиці, а значення розділено комами. Його відкриває будь-який редактор, Excel чи Google Таблиці, а на наступному уроці ви покажете точки з цього файлу на карті.

> 💁 Тут ви використовуєте ті самі прийоми, що й в [уроці 4 проєкту «Початок роботи»](../../../1-getting-started/lessons/4-connect-internet/README.md): MQTT-клієнт `paho-mqtt` 2.x, тему `<ID>/telemetry` і серверний код, що працює на вашому комп'ютері.

## Надсилання GPS-даних через MQTT

### Завдання: надішліть GPS-дані на MQTT-брокер

1. Відкрийте у VS Code проєкт `gps-sensor` з минулого уроку. Переконайтеся, що в терміналі активовано віртуальне середовище і застосунок CounterFit запущено з GPS-сенсором на порту `/dev/ttyAMA0`.

1. Встановіть MQTT-пакет:

    ```sh
    pip install "paho-mqtt>=2.1"
    ```

1. Додайте ці імпорти на початок файлу `app.py` разом з іншими:

    ```python
    import json
    import paho.mqtt.client as mqtt
    ```

1. Після імпортів додайте код підключення до MQTT-брокера:

    ```python
    id = '<ID>'

    client_name = id + 'gps_sensor_client'
    client_telemetry_topic = id + '/telemetry'


    def handle_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print('Не вдалося підключитися до MQTT:', reason_code)
            return

        print('Підключено до MQTT!')


    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
    mqtt_client.on_connect = handle_connect
    mqtt_client.connect('test.mosquitto.org')
    mqtt_client.loop_start()
    ```

    Замініть `<ID>` на унікальний ідентифікатор, наприклад той самий, що ви використовували в уроці 4 проєкту «Початок роботи». Пристрій і сервер мають використовувати однаковий ID, а інші студенти — різні.

1. Перейменуйте функцію `print_gps_data` на `send_gps_data` (і її виклик у циклі `while`), а рядок з `print` у кінці функції замініть на такий код:

    ```python
    telemetry = json.dumps({'gps': {'lat': lat, 'lon': lon}})
    print('Надсилаю телеметрію:', telemetry)
    mqtt_client.publish(client_telemetry_topic, telemetry)
    ```

    Цей код записує GPS-координати в JSON-документ у тому самому форматі, що й в Azure-версії уроку, і публікує його в MQTT-тему телеметрії.

1. Замініть `time.sleep(1)` у кінці циклу `while True:` на:

    ```python
    time.sleep(5)
    ```

    Так пристрій надсилатиме координати раз на 5 секунд. В Azure-версії уроку дані надсилають раз на хвилину, щоб не вичерпати денний ліміт повідомлень IoT Hub. Публічний MQTT-брокер такого ліміту не має, а з коротшим інтервалом результат видно швидше.

1. Запустіть код:

    ```sh
    python app.py
    ```

    ```output
    (.venv) ➜  gps-sensor python app.py
    Підключено до MQTT!
    Надсилаю телеметрію: {"gps": {"lat": 50.4501, "lon": 30.5234}}
    Надсилаю телеметрію: {"gps": {"lat": 50.4501, "lon": 30.5234}}
    ```

> 💁 Цей код є в папці [code-local/virtual-device](code-local/virtual-device).

## Збереження GPS-даних у CSV-файл

### Завдання: напишіть серверний код, який зберігає GPS-дані

1. Створіть нову папку `gps-server`, віртуальне середовище в ній і встановіть MQTT-пакет. Так само ви створювали папку `nightlight-server` в [уроці 4 проєкту «Початок роботи»](../../../1-getting-started/lessons/4-connect-internet/README.md):

    ```sh
    mkdir gps-server
    cd gps-server
    python3 -m venv .venv
    source ./.venv/bin/activate
    pip install "paho-mqtt>=2.1"
    ```

    > 💁 У Windows створюйте середовище командою `py -m venv .venv` і активуйте його командою `.venv\Scripts\activate.bat` (у командному рядку) або `.\.venv\Scripts\Activate.ps1` (у PowerShell).

1. Створіть у цій папці файл `app.py`, відкрийте папку у VS Code (`code .`) і додайте в `app.py` такий код:

    ```python
    import csv
    import json
    import os
    import time
    from datetime import datetime, timezone

    import paho.mqtt.client as mqtt

    id = '<ID>'

    client_name = id + 'gps_server'
    client_telemetry_topic = id + '/telemetry'

    data_file = 'gps_data.csv'
    ```

    Замініть `<ID>` на той самий ідентифікатор, що й у коді пристрою.

    `data_file` — назва CSV-файлу, у який сервер записуватиме GPS-точки. Файл з'явиться в поточній папці.

1. Нижче додайте функцію, яка дописує одну GPS-точку в CSV-файл:

    ```python
    def save_gps_data(gps):
        timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
        new_file = not os.path.exists(data_file)

        with open(data_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if new_file:
                writer.writerow(['timestamp', 'lat', 'lon'])
            writer.writerow([timestamp, gps['lat'], gps['lon']])

        print('Записано рядок:', timestamp, gps['lat'], gps['lon'])
    ```

    Функція бере поточний час у UTC, як-от `2026-10-02T09:15:00+00:00`. Це аналог часу постановки в чергу (`enqueuedtime`), який в Azure-версії записують у блоб.

    Файл відкривається в режимі `'a'` (append, дописування), тож нові рядки додаються в кінець, а старі дані не стираються. Якщо файлу ще не було, спочатку записується рядок заголовків `timestamp,lat,lon`. Модуль `csv` сам правильно форматує значення й розставляє коми.

1. Додайте код, який підписується на тему телеметрії й зберігає кожне отримане повідомлення:

    ```python
    def handle_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print('Не вдалося підключитися до MQTT:', reason_code)
            return

        print('Підключено до MQTT!')
        client.subscribe(client_telemetry_topic)


    def handle_telemetry(client, userdata, message):
        payload = json.loads(message.payload.decode())
        print('Отримано повідомлення:', payload)
        save_gps_data(payload['gps'])


    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
    mqtt_client.on_connect = handle_connect
    mqtt_client.on_message = handle_telemetry
    mqtt_client.connect('test.mosquitto.org')
    mqtt_client.loop_start()

    while True:
        time.sleep(2)
    ```

    Як і в серверному коді нічника, підписка відбувається в `handle_connect`, тож після перепідключення до брокера сервер знову підпишеться на тему. Для кожного повідомлення викликається `handle_telemetry`, яка розбирає JSON і передає GPS-координати у `save_gps_data`.

1. Запустіть сервер, а в іншому терміналі — код пристрою, якщо він ще не працює:

    ```sh
    python app.py
    ```

    ```output
    (.venv) ➜  gps-server python app.py
    Підключено до MQTT!
    Отримано повідомлення: {'gps': {'lat': 50.4501, 'lon': 30.5234}}
    Записано рядок: 2026-10-02T09:15:00+00:00 50.4501 30.5234
    Отримано повідомлення: {'gps': {'lat': 50.4501, 'lon': 30.5234}}
    Записано рядок: 2026-10-02T09:15:05+00:00 50.4501 30.5234
    ```

1. Змініть координати в CounterFit (або задайте NMEA-речення чи GPX-файл з маршрутом), щоб «проїхатися» кількома точками.

### Завдання: перевірте збережені дані

1. Відкрийте файл `gps_data.csv` у VS Code. Ви побачите приблизно таке:

    ```output
    timestamp,lat,lon
    2026-10-02T09:15:00+00:00,50.4501,30.5234
    2026-10-02T09:15:05+00:00,50.4501,30.5234
    2026-10-02T09:15:10+00:00,50.4547,30.5238
    ```

    Кожен рядок — одна GPS-точка, так само як кожен блоб в Azure-версії.

1. Зупиніть сервер і запустіть знову. Нові рядки допишуться в кінець файлу, а старі залишаться. Це і є збереження даних для теплого шляху: на наступному уроці ви покажете ці точки на карті.

> 💁 Цей код є в папці [code-local/server](code-local/server).

😀 Ви зберегли GPS-дані зі свого пристрою!
