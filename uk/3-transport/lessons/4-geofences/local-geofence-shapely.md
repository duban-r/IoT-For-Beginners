# Геозони: локальний варіант (GeoJSON і shapely)

У цій частині уроку ви задасте геозону як GeoJSON-багатокутник і перевірятимете кожну GPS-точку від свого віртуального пристрою: всередині вона чи поза геозоною. Усе працює на вашому комп'ютері, обліковий запис Azure не потрібен:

| Azure (історія й демо викладача) | Локальний варіант |
| --- | --- |
| Геозону завантажують в Azure Maps (Data API v1, виведено з експлуатації) | Геозона лежить у файлі `geofence.json` |
| Точку перевіряють запитом до Spatial API (виведено з експлуатації) | Точку перевіряє Python-бібліотека [shapely](https://shapely.readthedocs.io) |
| Окремий тригер Azure Functions зі своєю групою споживачів | Окремий Python-сервер, підписаний на ту саму MQTT-тему |

Знадобиться код пристрою з [локального варіанту уроку 2](../2-store-location-data/local-store-gps-data.md), який надсилає GPS-дані через MQTT.

## Як задати геозону

### Завдання: задайте геозону

1. Створіть на комп'ютері нову папку `gps-geofence` і відкрийте її у VS Code.

1. Створіть у цій папці файл `geofence.json` з GeoJSON-багатокутником. Ви перевірятимете його за допомогою віртуального GPS-сенсора, тож багатокутник має охоплювати координати, які ви задаєте в CounterFit. Наприклад, ось прямокутник навколо Майдану Незалежності в Києві:

    ```json
    {
      "type": "FeatureCollection",
      "features": [
        {
          "type": "Feature",
          "geometry": {
            "type": "Polygon",
            "coordinates": [
              [
                [30.5195, 50.4530],
                [30.5280, 50.4530],
                [30.5280, 50.4490],
                [30.5195, 50.4490],
                [30.5195, 50.4530]
              ]
            ]
          },
          "properties": {
            "geometryId": "1"
          }
        }
      ]
    }
    ```

    Багатокутник можна також намалювати в [GeoJSON.io](https://geojson.io/) навколо будь-якого іншого місця й скопіювати звідти JSON. Пам'ятайте, що кожна точка записується як `[довгота, широта]`, а остання точка збігається з першою.

    > 💁 Для shapely розділ `properties` з `geometryId` не обов'язковий, але він не заважає. Код нижче бере перший багатокутник з файлу.

## Перевірка точок щодо геозони

### Завдання: встановіть пакети

1. Створіть у папці `gps-geofence` віртуальне середовище й активуйте його, так само як для папки `gps-server` на уроці 2:

    ```sh
    python3 -m venv .venv
    source ./.venv/bin/activate
    ```

    > 💁 У Windows створюйте середовище командою `py -m venv .venv` і активуйте його командою `.venv\Scripts\activate.bat` (у командному рядку) або `.\.venv\Scripts\Activate.ps1` (у PowerShell).

1. Встановіть MQTT-пакет і shapely:

    ```sh
    pip install "paho-mqtt>=2.1" shapely
    ```

    Бібліотека `shapely` працює з геометричними фігурами: точками, лініями й багатокутниками. Вона вміє перевіряти, чи лежить точка всередині багатокутника, і обчислювати відстані між фігурами.

### Завдання: напишіть код перевірки геозони

1. Створіть у папці `gps-geofence` файл `app.py` і додайте в нього такий код:

    ```python
    import json
    import math
    import time

    import paho.mqtt.client as mqtt
    from shapely.affinity import scale
    from shapely.geometry import Point, shape

    id = '<ID>'

    client_name = id + 'geofence_server'
    client_telemetry_topic = id + '/telemetry'

    search_buffer = 50
    ```

    Замініть `<ID>` на той самий ідентифікатор, що й у коді пристрою.

    `search_buffer` — буфер пошуку в метрах. Як у Spatial API Azure Maps, точки, ближчі до межі геозони, ніж 50 м, отримають точну відстань.

1. Нижче додайте код, який завантажує геозону з файлу:

    ```python
    with open('geofence.json') as file:
        geofence = shape(json.load(file)['features'][0]['geometry'])
    ```

    Цей код читає GeoJSON, бере геометрію першого об'єкта `Feature`, а функція `shape` перетворює її на багатокутник shapely.

1. Додайте допоміжну функцію, яка переводить координати з градусів у метри:

    ```python
    def to_meters(geometry, lat):
        return scale(geometry, xfact=111_320 * math.cos(math.radians(lat)), yfact=110_540, origin=(0, 0))
    ```

    Shapely рахує відстані в тих самих одиницях, що й координати, тобто в градусах. Але градус — незручна одиниця: один градус широти — це приблизно 110,5 км, а один градус довготи — приблизно 111,3 км, помножені на косинус широти (що ближче до полюса, то коротші градуси довготи; у Києві це близько 71 км). Функція `scale` розтягує фігуру по осях з такими коефіцієнтами, і відстані стають приблизно метрами. Для відстаней у межах міста цього наближення цілком досить.

1. Додайте функцію, яка перевіряє одну точку:

    ```python
    def check_geofence(lat, lon):
        point = Point(lon, lat)
        distance = to_meters(geofence.exterior, lat).distance(to_meters(point, lat))

        if geofence.contains(point):
            distance = -distance

        if distance > search_buffer:
            print('Точка поза геозоною')
        elif distance > 0:
            print(f'Точка трохи поза геозоною, на відстані {distance:.0f} м')
        elif distance < -search_buffer:
            print('Точка всередині геозони')
        else:
            print(f'Точка трохи всередині геозони, на відстані {-distance:.0f} м від межі')
    ```

    Зверніть увагу: shapely, як і GeoJSON, очікує спочатку довготу, потім широту: `Point(lon, lat)`.

    `geofence.exterior` — це зовнішня межа багатокутника, тож `distance` — відстань від точки до найближчої точки на межі геозони. Якщо `geofence.contains(point)`, тобто точка всередині, відстань стає від'ємною, як у відповіді Spatial API. Далі код виводить одне з чотирьох повідомлень, як в оригінальному коді уроку:

    * далеко поза геозоною (у Spatial API це відстань 999);
    * поза геозоною, але ближче ніж 50 м до межі;
    * глибоко всередині геозони (у Spatial API це -999);
    * всередині геозони, але ближче ніж 50 м до межі.

1. Додайте код, який підписується на GPS-телеметрію й перевіряє кожну точку:

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
        check_geofence(payload['gps']['lat'], payload['gps']['lon'])


    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_name)
    mqtt_client.on_connect = handle_connect
    mqtt_client.on_message = handle_telemetry
    mqtt_client.connect('test.mosquitto.org')
    mqtt_client.loop_start()

    while True:
        time.sleep(2)
    ```

    > 💁 В Azure-версії для перевірки геозони створюють окрему групу споживачів, щоб кожна функція отримувала всі події. У MQTT це працює без додаткових налаштувань: кожен клієнт, підписаний на тему, отримує копію кожного повідомлення. Тому сервер `gps-server` з уроку 2 може й далі записувати точки в CSV, поки цей сервер перевіряє геозону. Головне, щоб у клієнтів були різні `client_id` (тут `geofence_server` і `gps_server`).

1. Запустіть CounterFit і код пристрою з уроку 2 (папка `gps-sensor`), а потім у новому терміналі з папки `gps-geofence` — цей сервер:

    ```sh
    python app.py
    ```

1. Змінюйте координати GPS-сенсора в CounterFit (джерело `Lat/Lon`, позначка **Repeat**, кнопка **Set**) і дивіться на вивід сервера. Наприклад, для прямокутника вище:

    | Широта | Довгота | Очікуваний результат |
    | --- | --- | --- |
    | 50.4510 | 30.52375 | всередині геозони |
    | 50.4527 | 30.5234 | трохи всередині, приблизно 33 м від межі |
    | 50.4533 | 30.5234 | трохи поза геозоною, приблизно 33 м |
    | 50.4547 | 30.5238 | поза геозоною |

    ```output
    (.venv) ➜  gps-geofence python app.py
    Підключено до MQTT!
    Отримано повідомлення: {'gps': {'lat': 50.451, 'lon': 30.52375}}
    Точка всередині геозони
    Отримано повідомлення: {'gps': {'lat': 50.4527, 'lon': 30.5234}}
    Точка трохи всередині геозони, на відстані 33 м від межі
    Отримано повідомлення: {'gps': {'lat': 50.4533, 'lon': 30.5234}}
    Точка трохи поза геозоною, на відстані 33 м
    Отримано повідомлення: {'gps': {'lat': 50.4547, 'lon': 30.5238}}
    Точка поза геозоною
    ```

> 💁 Цей код є в папці [code-local/geofence](code-local/geofence).

😀 Ваш пристрій тепер знає, коли вантажівка прибуває до місця призначення!
