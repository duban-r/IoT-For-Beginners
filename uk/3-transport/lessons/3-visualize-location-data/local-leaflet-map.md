# Візуалізація GPS-даних: локальний варіант (Leaflet і OpenStreetMap)

У цій частині уроку ви покажете на карті GPS-точки, збережені на минулому уроці у файл `gps_data.csv`. Обліковий запис Azure і ключі API не потрібні:

| Azure (демо викладача) | Локальний варіант |
| --- | --- |
| Карта Azure Maps (Web SDK v3) з ключем API | Бібліотека [Leaflet](https://leafletjs.com) з картою [OpenStreetMap](https://www.openstreetmap.org), без ключа |
| Точки зберігаються як JSON-блоби в Azure Storage | Точки зберігаються у файлі `gps_data.csv` |
| Вебсторінка завантажує блоби й перетворює їх на GeoJSON | Python-скрипт перетворює CSV на GeoJSON, а вебсторінка показує його |

## Перетворення CSV на GeoJSON

Leaflet, як і Azure Maps, вміє показувати дані у форматі GeoJSON. Тож спочатку перетворимо CSV-файл на GeoJSON.

### Завдання: перетворіть CSV-файл на GeoJSON

1. Створіть на комп'ютері нову папку `gps-map`.

1. Скопіюйте в неї файл `gps_data.csv` з папки `gps-server` з минулого уроку.

    > 💁 Якщо у вас немає власного файлу, візьміть приклад [gps_data.csv](code-local/gps-map/gps_data.csv): це маршрут вантажівки через центр Києва до Майдану Незалежності.

1. Відкрийте папку `gps-map` у VS Code і створіть у ній файл `csv_to_geojson.py` з таким кодом:

    ```python
    import csv
    import json

    features = []

    with open('gps_data.csv', newline='') as file:
        for row in csv.DictReader(file):
            features.append({
                'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [float(row['lon']), float(row['lat'])]
                },
                'properties': {
                    'timestamp': row['timestamp']
                }
            })

    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }

    with open('gps_data.js', 'w') as file:
        file.write('const gpsData = ' + json.dumps(geojson, indent=2) + ';\n')

    print('Записано точок:', len(features))
    ```

    `csv.DictReader` читає CSV-файл рядок за рядком і повертає кожен рядок як словник, ключами якого є заголовки стовпців: `timestamp`, `lat` і `lon`.

    Для кожного рядка код створює GeoJSON-об'єкт `Feature` з геометрією типу `Point`. Зверніть увагу на порядок координат: спочатку довгота (`lon`), потім широта (`lat`), як вимагає GeoJSON. Час точки зберігається у властивостях (`properties`) об'єкта, щоб показати його на карті.

    Усі об'єкти збираються в колекцію `FeatureCollection` і записуються у файл `gps_data.js` як JavaScript-змінна `gpsData`.

    > 💁 Чому `.js`, а не `.json`? Ви відкриватимете HTML-сторінку прямо з диска, подвійним клацанням. Браузери з міркувань безпеки не дають такій сторінці завантажувати інші файли через `fetch`, а от підключити скрипт тегом `<script>` дозволяють. Тому GeoJSON записується як скрипт, що оголошує змінну.

1. Запустіть скрипт у терміналі з папки `gps-map`. Сторонні пакети йому не потрібні, тож підійде будь-який Python 3.10 або новіший:

    ```sh
    python csv_to_geojson.py
    ```

    ```output
    ➜  gps-map python csv_to_geojson.py
    Записано точок: 12
    ```

    У папці з'явиться файл `gps_data.js`. Відкрийте його й подивіться на структуру GeoJSON. Можете також вставити вміст після `const gpsData = ` (без крапки з комою в кінці) на сайті [geojson.io](https://geojson.io) і перевірити, що точки стоять там, де треба.

## Показ точок на карті

### Завдання: покажіть GPS-точки на карті

1. Створіть у папці `gps-map` файл `index.html` з таким вмістом:

    ```html
    <!DOCTYPE html>
    <html>

    <head>
        <meta charset="utf-8">
        <title>GPS-трек</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <script src="gps_data.js"></script>
        <style>
            html,
            body,
            #myMap {
                width: 100%;
                height: 100%;
                margin: 0;
            }
        </style>
    </head>

    <body>
        <div id="myMap"></div>
    </body>

    </html>
    ```

    Як і в Azure-версії, карта завантажиться в `div` з ідентифікатором `myMap`, а стилі розтягують її на всю сторінку. У `<head>` підключено таблицю стилів і скрипт бібліотеки Leaflet, а також ваш файл `gps_data.js` з точками.

1. Перед закривальним тегом `</body>` додайте блок скрипту:

    ```html
    <script>
        const map = L.map('myMap');

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        const points = L.geoJSON(gpsData, {
            pointToLayer: (feature, latlng) => L.circleMarker(latlng, { radius: 6 }),
            onEachFeature: (feature, layer) => layer.bindPopup(feature.properties.timestamp)
        }).addTo(map);

        map.fitBounds(points.getBounds());
    </script>
    ```

    `L.map('myMap')` створює карту в `div` з ідентифікатором `myMap`.

    `L.tileLayer` додає шар тайлів — квадратних картинок 256×256 пікселів, з яких складається карта. Тайли завантажуються з серверів OpenStreetMap: `{z}` — рівень масштабу, `{x}` і `{y}` — номер тайла. Умови використання OpenStreetMap вимагають підпису (attribution) з посиланням на джерело, тож він обов'язковий.

    `L.geoJSON` створює шар з вашого GeoJSON. Для кожної точки `pointToLayer` малює коло (`circleMarker`) — аналог бульбашкового шару в Azure Maps. `onEachFeature` додає до кожного кола спливне вікно з часом цієї точки.

    `map.fitBounds` автоматично підбирає центр і масштаб карти так, щоб було видно всі точки. Тому, на відміну від Azure-версії, координати центру вказувати не треба.

1. Відкрийте файл `index.html` у браузері: двічі клацніть його у файловому менеджері або перетягніть у вікно браузера. Завантажиться карта з колами вздовж шляху вашого GPS-сенсора. Клацніть коло, щоб побачити час точки.

    > 💁 Якщо замість карти сіре поле, але кола видно, браузер не зміг завантажити тайли OpenStreetMap: перевірте підключення до Інтернету. Якщо не видно навіть кіл, відкрийте інструменти розробника (`F12`), вкладку **Console**, і подивіться на помилки. Найчастіша причина — файл `gps_data.js` не створено або він лежить в іншій папці.

1. Коли на минулому уроці з'являться нові точки, скопіюйте новий `gps_data.csv`, знову запустіть `python csv_to_geojson.py` і оновіть сторінку в браузері.

> 💁 Цей код є в папці [code-local/gps-map](code-local/gps-map).

😀 Ви показали шлях свого GPS-сенсора на карті!
