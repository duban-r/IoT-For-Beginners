# Класифікуйте зображення локально моделлю з Teachable Machine (локальний варіант)

У цій частині уроку ви класифікуєте зображення, зняте камерою віртуального пристрою, моделлю, яку натренували в Teachable Machine в [уроці 1](../1-train-fruit-detector/local-teachable-machine.md). Модель працюватиме просто на вашому комп'ютері, без хмари й без облікового запису Azure.

Для запуску моделі використаємо бібліотеку [LiteRT](https://pypi.org/project/ai-edge-litert/) (так тепер називається TensorFlow Lite) від Google. Вона значно менша за повний TensorFlow і встановлюється на Python 3.14.

## Підготуйте модель

### Завдання: скопіюйте модель у проєкт

1. Знайдіть файли `model_unquant.tflite` і `labels.txt`, які ви експортували з Teachable Machine в уроці 1.

1. Скопіюйте обидва файли в папку `fruit-quality-detector`, поруч із файлом `app.py`.

## Класифікуйте зображення

### Завдання: класифікуйте зображення з камери

1. Відкрийте папку `fruit-quality-detector` у VS Code і переконайтеся, що в терміналі активовано віртуальне середовище.

1. Встановіть pip-пакети для запуску моделі:

    ```sh
    pip install ai-edge-litert pillow numpy
    ```

    > 💁 Пакет `ai-edge-litert` для Python 3.14 доступний для Windows (64-bit), Linux і macOS на процесорах Apple (M1 і новіших). Якщо pip пише, що не знаходить відповідної версії (наприклад, на Mac з процесором Intel), скористайтеся способом із розділу [Якщо ai-edge-litert не встановлюється](#якщо-ai-edge-litert-не-встановлюється).

1. Додайте до інструкцій імпорту на початку файлу `app.py` такі рядки:

    ```python
    import numpy as np
    from PIL import Image, ImageOps
    from ai_edge_litert.interpreter import Interpreter
    ```

    `Interpreter` завантажує й запускає модель TensorFlow Lite, бібліотека Pillow (`PIL`) готує зображення, а `numpy` перетворює його на масив чисел для моделі.

1. Додайте в кінець файлу код, що завантажує модель і назви класів:

    ```python
    interpreter = Interpreter(model_path='model_unquant.tflite')
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]

    with open('labels.txt', encoding='utf-8') as labels_file:
        labels = [line.strip().split(' ', 1)[-1] for line in labels_file if line.strip()]
    ```

    Цей код завантажує модель і дізнається, куди передавати зображення (`input_details`) і звідки брати результат (`output_details`). У файлі `labels.txt` кожен рядок має вигляд `0 ripe`, тому код відкидає номер і залишає лише назву класу.

1. Додайте код, що готує зображення для моделі:

    ```python
    height, width = input_details['shape'][1:3]

    image.seek(0)
    picture = Image.open(image).convert('RGB')
    picture = ImageOps.fit(picture, (width, height), Image.Resampling.LANCZOS)
    data = np.asarray(picture, dtype=np.float32) / 127.5 - 1
    data = np.expand_dims(data, axis=0)
    ```

    Модель Teachable Machine працює із зображеннями 224x224, тому код вирізає з центру знімка квадрат і зменшує його до цього розміру. Потім значення кольорів кожного пікселя (від 0 до 255) перераховуються в діапазон від -1 до 1, як очікує модель. Останній рядок загортає зображення в масив з одного зображення, бо модель приймає пакети зображень.

    > 💁 Так само, як Custom Vision працює з зображеннями 227x227, ця модель бачить лише маленьке зображення 224x224. Тому фрукт має займати значну частину кадру.

1. Додайте код, що запускає модель і виводить результати:

    ```python
    interpreter.set_tensor(input_details['index'], data)
    interpreter.invoke()
    probabilities = interpreter.get_tensor(output_details['index'])[0]

    for label, probability in zip(labels, probabilities):
        print(f'{label}:\t{probability * 100:.2f}%')
    ```

    Цей код передає зображення в модель, запускає її і отримує ймовірності для кожного класу. Як і в Custom Vision, імовірності — це дійсні числа від 0 до 1, тож код множить їх на 100 і виводить у відсотках.

1. Переконайтеся, що CounterFit запущено, а для камери `Picamera` встановлено зображення фрукта (наприклад, з папки [images/testing](../1-train-fruit-detector/images/testing) уроку 1) або вебкамеру. Запустіть код:

    ```sh
    python app.py
    ```

    У консолі ви побачите результат:

    ```output
    (.venv) ➜  fruit-quality-detector python app.py
    INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
    ripe:   96.60%
    unripe: 3.40%
    ```

    Рядок `INFO: ...` виводить сама бібліотека LiteRT, це не помилка. Ваші відсотки будуть іншими, бо залежать від вашої моделі й зображення.

    Спробуйте встановити в CounterFit інше зображення (наприклад, недостиглого банана) і запустіть код ще раз.

> 💁 Цей код є в папці [code-local/virtual-iot-device](code-local/virtual-iot-device). Файли моделі в репозиторії немає: використовуйте модель, яку ви натренували самі.

😀 Ваш класифікатор якості фруктів працює локально!

## Якщо ai-edge-litert не встановлюється

Якщо пакет `ai-edge-litert` не встановлюється на вашому комп'ютері, класифікуйте знімок у браузері:

1. Запустіть код із [virtual-device-camera.md](virtual-device-camera.md) (папка [code-camera/virtual-iot-device](code-camera/virtual-iot-device)). Він збереже знімок камери у файл `image.jpg`.

1. Відкрийте свій проєкт у Teachable Machine (меню ☰ → **Open project from file**, або натренуйте модель заново за [інструкцією з уроку 1](../1-train-fruit-detector/local-teachable-machine.md)).

1. У блоці **Preview** виберіть **File** замість **Webcam** і перетягніть туди файл `image.jpg`. У розділі **Output** ви побачите ймовірності для `ripe` і `unripe`.

## Покращте модель

Як і з Custom Vision, модель може помилятися на знімках із камери пристрою, бо тренувалася на інших зображеннях.

### Завдання: покращте модель

1. Зробіть віртуальною камерою кілька знімків достиглих і недостиглих фруктів. Після кожного запуску перейменуйте файл `image.jpg` (наприклад, на `ripe-1.jpg` чи `unripe-1.jpg`), щоб наступний знімок його не перезаписав.

1. Відкрийте свій проєкт у Teachable Machine і завантажте ці знімки кнопкою **Upload** у відповідні класи.

1. Натисніть **Train Model**, а потім знову експортуйте модель (**Export Model** → **Tensorflow Lite** → **Floating point** → **Download my model**).

1. Замініть файли `model_unquant.tflite` і `labels.txt` у папці `fruit-quality-detector` на нові та перезапустіть застосунок.

1. Повторюйте ці кроки, доки результати передбачень вас не влаштують.
