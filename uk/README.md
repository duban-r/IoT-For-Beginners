# IoT для початківців (українська адаптація)

Українська адаптація курсу [IoT for Beginners](https://github.com/microsoft/IoT-For-Beginners) від Microsoft для проведення занять. Код оновлено під сучасні версії Python (3.11–3.14) і бібліотек, а застарілі хмарні сервіси замінюються актуальними.

## Стан

| Розділ | Урок | Стан |
| --- | --- | --- |
| 1. Початок роботи | [1. Вступ до IoT](1-getting-started/lessons/1-introduction-to-iot/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| | [2. Глибше про IoT](1-getting-started/lessons/2-deeper-dive/README.md) | Готово |
| | [3. Сенсори й актуатори](1-getting-started/lessons/3-sensors-and-actuators/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| | [4. Підключіть свій пристрій до Інтернету](1-getting-started/lessons/4-connect-internet/README.md) | Готово (шлях Raspberry Pi / віртуальний пристрій) |
| Усі розділи | [Тести до уроків](quiz-app/README.md) | Перекладено (застосунок ще не розгорнуто) |
| Решта | | За [планом](docs/audit-and-plan.md) |

## Як адаптовано

* Текст уроків взято з автоматичного українського перекладу в оригінальному репозиторії, вичитано й виправлено (в автоперекладі були обрізані фрагменти й неробочі посилання).
* Код перевірено на Python 3.11–3.14 з віртуальним пристроєм CounterFit. Шлях Raspberry Pi оновлено під Raspberry Pi OS Bookworm, але на справжньому залізі ще не перевірено.
* Шлях Wio Terminal (Arduino) поки веде на англійський оригінал.
* Щоб перед заняттям перевірити CounterFit на своєму комп'ютері, запустіть `counterfit`, а в іншому терміналі [tools/counterfit_selftest.py](tools/counterfit_selftest.py) (потрібні також `pip install counterfit-shims-seeed-python-dht counterfit-shims-serial counterfit-shims-picamera counterfit-shims-rpi-vl53l0x pynmea2 pillow`). Скрипт створює всі віртуальні сенсори й актуатори курсу та перевіряє кожен.

## Ліцензія

Оригінальний курс © Microsoft, ліцензія MIT (див. [LICENSE](LICENSE)). Зображення та скетчноти належать їхнім авторам, зазначеним в оригінальному курсі.
