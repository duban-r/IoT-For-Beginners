# Текст у мовлення: віртуальний IoT-пристрій

> 👩‍🏫 Цю частину показує викладач (демо). Студенти виконують [локальний варіант](local-text-to-speech.md).

У цій частині уроку ви напишете код, який перетворює текст на мовлення за допомогою сервісу Speech.

## Перетворення тексту на мовлення

SDK сервісу Speech, яким ви в минулому уроці перетворювали мовлення на текст, уміє перетворювати й текст назад на мовлення. Запитуючи мовлення, треба вказати голос, бо мовлення можна згенерувати різними голосами.

Кожна мова підтримує кілька голосів, і список підтримуваних голосів для кожної мови можна отримати через SDK сервісу Speech.

### Завдання: перетворіть текст на мовлення

1. Відкрийте проєкт `smart-timer` у VS Code і переконайтеся, що в терміналі активовано віртуальне середовище.

1. Імпортуйте `SpeechSynthesizer` з пакета `azure.cognitiveservices.speech`, додавши його до наявних імпортів:

    ```python
    from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, SpeechSynthesizer
    ```

1. Над функцією `say` створіть налаштування мовлення для синтезатора:

    ```python
    speech_config = SpeechConfig(subscription=speech_api_key,
                                 region=location)
    speech_config.speech_synthesis_language = language
    speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
    ```

    Тут використовуються ті самі ключ API, розташування й мова, що й у розпізнавача.

1. Під цим кодом додайте такий код, щоб отримати голос і задати його в налаштуваннях:

    ```python
    voices = speech_synthesizer.get_voices_async().get().voices
    first_voice = next(x for x in voices if x.locale.lower() == language.lower())
    speech_config.speech_synthesis_voice_name = first_voice.short_name
    ```

    Цей код отримує список усіх доступних голосів і знаходить перший голос для мови, яку ви використовуєте.

    > 💁 Повний список підтримуваних голосів є в [документації про підтримку мов і голосів на Microsoft Learn](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts). Якщо хочете використати конкретний голос, можете прибрати цей код і задати назву голосу з документації напряму. Наприклад:
    >
    > ```python
    > speech_config.speech_synthesis_voice_name = 'uk-UA-PolinaNeural'
    > ```

1. Замініть вміст функції `say` кодом, який формує SSML для відповіді:

    ```python
        ssml =  f'<speak version=\'1.0\' xml:lang=\'{language}\'>'
        ssml += f'<voice xml:lang=\'{language}\' name=\'{first_voice.short_name}\'>'
        ssml += text
        ssml += '</voice>'
        ssml += '</speak>'
    ```

1. Під цим кодом зупиніть розпізнавання мовлення, вимовте SSML і знову запустіть розпізнавання:

    ```python
        recognizer.stop_continuous_recognition()
        speech_synthesizer.speak_ssml(ssml)
        recognizer.start_continuous_recognition()
    ```

    Розпізнавання зупиняється, поки текст вимовляється, щоб повідомлення про запуск таймера не було розпізнане, передане на розуміння мови й, можливо, сприйняте як запит поставити новий таймер.

    > 💁 Можете перевірити це, закоментувавши рядки, що зупиняють і знову запускають розпізнавання. Поставте один таймер, і може виявитися, що повідомлення ставить новий таймер, який спричиняє нове повідомлення, що ставить ще один таймер, і так без кінця!

1. Запустіть застосунок. Поставте кілька таймерів, і ви почуєте голосову відповідь про те, що таймер поставлено, а потім ще одну, коли таймер завершиться.

    > 💁 Якщо голос неприродно читає скорочення «хв» і «с», замініть їх у функціях `announce_timer` і `create_timer` повними словами.

> 💁 Цей код є в папці [code-spoken-response/virtual-iot-device](code-spoken-response/virtual-iot-device).

😀 Ваша програма-таймер запрацювала!
