# Класифікуйте зображення класифікатором на IoT Edge: віртуальне IoT-обладнання та Raspberry Pi

> 👩‍🏫 Цю частину показує викладач (демо). Студенти виконують локальний варіант: [Ваш комп'ютер як периферійний пристрій](local-edge.md).

У цій частині уроку ви використаєте класифікатор зображень, що працює на пристрої IoT Edge.

## Використання класифікатора на IoT Edge

IoT-пристрій можна перенаправити на класифікатор зображень на IoT Edge. URL-адреса класифікатора — `http://<IP address or name>/image`, де `<IP address or name>` потрібно замінити на IP-адресу або ім'я хоста комп'ютера, на якому працює IoT Edge.

Python-бібліотека для Custom Vision працює лише з моделями в хмарі, а не з моделями на IoT Edge. Тому для виклику класифікатора доведеться використати REST API.

### Завдання: використайте класифікатор на IoT Edge

1. Відкрийте проєкт `fruit-quality-detector` у VS Code, якщо він ще не відкритий. Якщо ви використовуєте віртуальний IoT-пристрій, переконайтеся, що віртуальне середовище активовано.

1. Відкрийте файл `app.py` і видаліть інструкції імпорту з `azure.cognitiveservices.vision.customvision.prediction` і `msrest.authentication`.

1. Додайте на початок файлу такий імпорт:

    ```python
    import requests
    ```

    > 💁 Пакет `requests` встановлюється разом із пакетами CounterFit. Якщо його немає, встановіть його командою `pip install requests`.

1. Видаліть увесь код після збереження зображення у файл, від рядка `image_file.write(image.read())` до кінця файлу.

1. Додайте в кінець файлу такий код:

    ```python
    prediction_url = '<URL>'
    headers = {
        'Content-Type' : 'application/octet-stream'
    }
    image.seek(0)
    response = requests.post(prediction_url, headers=headers, data=image)
    results = response.json()
    
    for prediction in results['predictions']:
        print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')
    ```

    Замініть `<URL>` на URL-адресу свого класифікатора.

    Цей код надсилає класифікатору REST-запит POST, передаючи зображення в тілі запиту. Результати повертаються у форматі JSON, який декодується, щоб вивести ймовірності.

1. Запустіть код, спрямувавши камеру на фрукти, або встановивши відповідне зображення, або тримаючи фрукт перед вебкамерою, якщо використовуєте віртуальне IoT-обладнання. У консолі ви побачите результат:

    ```output
    (.venv) ➜  fruit-quality-detector python app.py
    ripe:   56.84%
    unripe: 43.16%
    ```

> 💁 Цей код є в папці [code-classify/virtual-iot-device](code-classify/virtual-iot-device). Код для Raspberry Pi є в [оригінальному репозиторії](https://github.com/microsoft/IoT-For-Beginners/tree/main/4-manufacturing/lessons/3-run-fruit-detector-edge/code-classify/pi) (ще не адаптовано).

😀 Ваша програма-класифікатор якості фруктів запрацювала!
