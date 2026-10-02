# IoT для початківців (українська адаптація)

Українська адаптація курсу [IoT for Beginners](https://github.com/microsoft/IoT-For-Beginners) від Microsoft для проведення занять. Код оновлено під сучасні версії Python (рекомендовано 3.14) і бібліотек, а застарілі хмарні сервіси замінюються актуальними.

## Стан

| Розділ | Урок | Стан |
| --- | --- | --- |
| 1. Початок роботи | [1. Вступ до IoT](1-getting-started/lessons/1-introduction-to-iot/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| | [2. Глибше про IoT](1-getting-started/lessons/2-deeper-dive/README.md) | Готово |
| | [3. Сенсори й актуатори](1-getting-started/lessons/3-sensors-and-actuators/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| | [4. Підключіть свій пристрій до Інтернету](1-getting-started/lessons/4-connect-internet/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| Усі розділи | [Тести до уроків](quiz-app/README.md) | Перекладено (застосунок ще не розгорнуто) |
| 2. Ферма | [Прогнозування росту рослин за допомогою IoT](2-farm/lessons/1-predict-plant-growth/README.md) | Готово (віртуальний пристрій) |
|  | [Вимірювання вологості ґрунту](2-farm/lessons/2-detect-soil-moisture/README.md) | Готово (віртуальний пристрій) |
|  | [Автоматичний полив рослин](2-farm/lessons/3-automated-plant-watering/README.md) | Готово (віртуальний пристрій) |
|  | [Перенесіть свою рослину в хмару](2-farm/lessons/4-migrate-your-plant-to-the-cloud/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Перенесіть логіку застосунку в хмару](2-farm/lessons/5-migrate-application-to-the-cloud/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Захистіть свою рослину](2-farm/lessons/6-keep-your-plant-secure/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
| 3. Транспорт | [Відстеження місцеположення](3-transport/lessons/1-location-tracking/README.md) | Готово (віртуальний пристрій) |
|  | [Зберігання даних про місцеположення](3-transport/lessons/2-store-location-data/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Візуалізація даних про місцеположення](3-transport/lessons/3-visualize-location-data/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Геозони](3-transport/lessons/4-geofences/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
| 4. Виробництво | [Навчіть детектор якості фруктів](4-manufacturing/lessons/1-train-fruit-detector/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Перевірте якість фруктів за допомогою IoT-пристрою](4-manufacturing/lessons/2-check-fruit-from-device/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Запустіть детектор фруктів на периферії](4-manufacturing/lessons/3-run-fruit-detector-edge/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
| 6. Побутові пристрої | [Розпізнавання мовлення за допомогою IoT-пристрою](6-consumer/lessons/1-speech-recognition/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Розуміння мови](6-consumer/lessons/2-language-understanding/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
|  | [Встановлення таймера й голосова відповідь](6-consumer/lessons/3-spoken-feedback/README.md) | Готово (хмара Azure як демо викладача, студенти виконують локальний варіант) |
| 5. Роздрібна торгівля; 4.4, 6.4 | | Не входять до курсу, див. [оригінал](https://github.com/microsoft/IoT-For-Beginners) |

## Як адаптовано

* Текст уроків взято з автоматичного українського перекладу в оригінальному репозиторії, вичитано й виправлено (в автоперекладі були обрізані фрагменти й неробочі посилання).
* Код перевірено на Python 3.11–3.14 з віртуальним пристроєм CounterFit. Шлях Raspberry Pi оновлено під Raspberry Pi OS Bookworm, але на справжньому залізі ще не перевірено.
* Шлях Wio Terminal (Arduino) поки веде на англійський оригінал. У розділах 2–6 так само на оригінал веде й шлях Raspberry Pi: студенти працюють лише з віртуальним пристроєм.
* Частини, які потребують Azure, позначено як демо викладача. Для кожної є локальний варіант (файли `local-*.md`), що працює без облікового запису Azure.
* Щоб перед заняттям перевірити CounterFit на своєму комп'ютері, запустіть `counterfit`, а в іншому терміналі [tools/counterfit_selftest.py](tools/counterfit_selftest.py) (потрібні також `pip install counterfit-shims-seeed-python-dht counterfit-shims-serial counterfit-shims-picamera counterfit-shims-rpi-vl53l0x pynmea2 pillow`). Скрипт створює всі віртуальні сенсори й актуатори курсу та перевіряє кожен.

## Ліцензія

Оригінальний курс © Microsoft, ліцензія MIT (див. [LICENSE](LICENSE)). Зображення та скетчноти належать їхнім авторам, зазначеним в оригінальному курсі.
