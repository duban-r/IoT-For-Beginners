# Мовлення в текст: віртуальний IoT-пристрій

> 👩‍🏫 Цю частину показує викладач (демо). Студенти виконують [локальний варіант](local-text-input.md).

У цій частині уроку ви напишете код, який перетворює мовлення, записане з мікрофона, на текст за допомогою сервісу Speech.

## Перетворення мовлення на текст

У Windows, Linux і macOS можна використати Python SDK сервісу Speech, щоб слухати мікрофон і перетворювати на текст усе мовлення, яке буде виявлено. SDK слухає безперервно, стежить за рівнем звуку й надсилає мовлення на перетворення в текст, коли рівень звуку падає, наприклад наприкінці фрази.

### Завдання: перетворіть мовлення на текст

1. Створіть на комп'ютері новий Python-застосунок у папці `smart-timer` з одним файлом `app.py` і віртуальним середовищем Python.

1. Встановіть пакет Pip для сервісу Speech. Переконайтеся, що встановлюєте його з терміналу з активованим віртуальним середовищем.

    ```sh
    pip install azure-cognitiveservices-speech
    ```

    > ⚠️ Якщо ви отримаєте таку помилку:
    >
    > ```output
    > ERROR: Could not find a version that satisfies the requirement azure-cognitiveservices-speech (from versions: none)
    > ERROR: No matching distribution found for azure-cognitiveservices-speech
    > ```
    >
    > оновіть Pip такою командою, а потім спробуйте встановити пакет ще раз:
    >
    > ```sh
    > pip install --upgrade pip
    > ```

    > 💁 У Linux для роботи SDK також потрібні системні бібліотеки OpenSSL і ALSA (наприклад, пакети `libssl-dev` і `libasound2` в Ubuntu). Подробиці є в [документації SDK сервісу Speech](https://learn.microsoft.com/azure/ai-services/speech-service/quickstarts/setup-platform?pivots=programming-language-python).

1. Додайте такі імпорти у файл `app.py`:

    ```python
    import time
    from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer
    ```

    Це імпортує класи, потрібні для розпізнавання мовлення.

1. Додайте такий код, щоб оголосити налаштування:

    ```python
    speech_api_key = '<key>'
    location = '<location>'
    language = '<language>'

    recognizer_config = SpeechConfig(subscription=speech_api_key,
                                     region=location,
                                     speech_recognition_language=language)
    ```

    Замініть `<key>` на ключ API вашого ресурсу Speech. Замініть `<location>` на розташування, яке ви використали під час створення ресурсу Speech.

    Замініть `<language>` на назву локалі мови, якою ви говоритимете, наприклад `uk-UA` для української, `en-GB` для британської англійської або `zh-HK` для кантонської. Список підтримуваних мов і назви їхніх локалей є в [документації про підтримку мов і голосів на Microsoft Learn](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=stt).

    Ці налаштування використовуються для створення об'єкта `SpeechConfig`, яким налаштовується сервіс Speech.

1. Додайте такий код, щоб створити розпізнавач мовлення:

    ```python
    recognizer = SpeechRecognizer(speech_config=recognizer_config)
    ```

1. Розпізнавач мовлення працює у фоновому потоці: слухає звук і перетворює мовлення на текст. Отримати текст можна через функцію зворотного виклику (callback) — функцію, яку ви визначаєте й передаєте розпізнавачу. Щоразу, коли виявлено мовлення, викликається ця функція. Додайте такий код, щоб визначити функцію зворотного виклику й передати її розпізнавачу, а також визначити функцію, яка обробляє текст і виводить його в консоль:

    ```python
    def process_text(text):
        print(text)

    def recognized(args):
        process_text(args.result.text)
    
    recognizer.recognized.connect(recognized)
    ```

1. Розпізнавач починає слухати лише тоді, коли ви явно його запустите. Додайте такий код, щоб запустити розпізнавання. Воно працює у фоні, тому застосунку також потрібен нескінченний цикл із паузою, щоб він не завершувався.

    ```python
    recognizer.start_continuous_recognition()

    while True:
        time.sleep(1)
    ```

1. Запустіть застосунок. Говоріть у мікрофон, і перетворений на текст звук з'являтиметься в консолі.

    ```output
    (.venv) ➜  smart-timer python3 app.py
    Привіт, світе.
    Ласкаво просимо до курсу IoT для початківців.
    ```

    Спробуйте різні речення, зокрема такі, де слова звучать однаково, але мають різне значення. Наприклад, якщо говорите англійською, скажіть «I want to buy two bananas and an apple too» і зверніть увагу, що сервіс правильно вибере to, two і too з огляду на контекст, а не лише на звучання.

> 💁 Цей код є в папці [code-speech-to-text/virtual-iot-device](code-speech-to-text/virtual-iot-device).

😀 Ваша програма для перетворення мовлення на текст запрацювала!
