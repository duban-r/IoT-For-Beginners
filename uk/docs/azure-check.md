# Що перевірити в Azure for Students для курсу IoT

Мета: з'ясувати, які сервіси з курсу ще створюються й працюють на студентській підписці. Усе на безкоштовних рівнях (F0/F1/Free), очікувана вартість близько $0. Наприкінці видалити групу ресурсів.

Підготовка: `az login`, `az account show` (має бути підписка Azure for Students), потім:

```sh
az extension add --name azure-iot
az group create --name iot-check --location westeurope
```

Регіон: якщо westeurope заборонено політикою підписки (`RequestDisallowedByAzure`), записати дозволені регіони з тексту помилки й повторити з одним із них.

| # | Сервіс (розділ курсу) | Команда | Що записати |
| --- | --- | --- | --- |
| 1 | IoT Hub, рівень F1 (розділи 2, 3, 5, 6) | `az iot hub create --resource-group iot-check --sku F1 --partition-count 2 --name iot-check-<ім'я>` | Створився чи ні, текст помилки. F1 лише один на підписку |
| 2 | Пристрій і рядок підключення | `az iot hub device-identity create --device-id test --hub-name <hub>` і `az iot hub device-identity connection-string show --device-id test --hub-name <hub>` | Чи повернувся рядок `HostName=...` |
| 3 | Надсилання й читання телеметрії | `az iot device send-d2c-message --hub-name <hub> --device-id test --data '{"t":1}'`, у другому терміналі `az iot hub monitor-events --hub-name <hub>` | Чи з'явилося повідомлення |
| 4 | Storage, Standard_LRS (розділи 2, 3) | `az storage account create -g iot-check -n iotcheck<цифри> --sku Standard_LRS` | Створився чи ні |
| 5 | Azure Functions, Python (розділи 2, 3, 6) | `az functionapp create -g iot-check --consumption-plan-location westeurope --runtime python --runtime-version 3.12 --functions-version 4 --os-type linux --storage-account <storage> -n iot-check-func-<ім'я>` | Створився чи ні; якщо 3.12 відхилено, спробувати 3.11 |
| 6 | Azure Maps, Gen2 (розділ 3) | `az maps account create -g iot-check -n iot-check-maps --sku G2 --kind Gen2 --accept-tos` | Створився чи ні |
| 7 | Custom Vision, F0 (розділи 4, 5) | `az cognitiveservices account create -g iot-check -n iot-check-cv --kind CustomVision.Training --sku F0 --location westeurope --yes` | Створився чи ні; чи відкривається customvision.ai з цим акаунтом |
| 8 | Speech, F0 (розділ 6) | `az cognitiveservices account create -g iot-check -n iot-check-speech --kind SpeechServices --sku F0 --location westeurope --yes` | Створився чи ні |
| 9 | Translator, F0 (розділ 6) | `az cognitiveservices account create -g iot-check -n iot-check-tr --kind TextTranslation --sku F0 --location global --yes` | Створився чи ні |
| 10 | Language/CLU, F0 (розділ 6, заміна LUIS) | `az cognitiveservices account create -g iot-check -n iot-check-lang --kind TextAnalytics --sku F0 --location westeurope --yes` | Створився чи ні; чи відкривається language.cognitive.azure.com |
| 11 | LUIS (контроль) | `az cognitiveservices account create -g iot-check -n iot-check-luis --kind LUIS --sku F0 --location westus --yes` | Очікувано помилка, бо LUIS вимкнено 1.10.2025 |
| 12 | Кредит | `az consumption usage list --top 5` або сторінка Azure for Students | Скільки кредиту залишилось |

Прибирання наприкінці (обов'язково):

```sh
az group delete --name iot-check --yes --no-wait
```

Результат: таблиця «# — створилось / помилка (текст)». Ключі й рядки підключення в чат не копіювати.
