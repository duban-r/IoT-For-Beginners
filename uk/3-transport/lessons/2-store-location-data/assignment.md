# Дослідіть прив'язки функцій

## Інструкції

Прив'язки функцій (function bindings) дають змогу коду зберігати блоби в blob-сховищі, просто повертаючи їх із функції. Обліковий запис Azure Storage, контейнер та інші параметри задають у декораторі прив'язки у файлі `function_app.py` (у старій моделі програмування v1 — у файлі `function.json`).

Коли ви працюєте з Azure чи іншими технологіями Microsoft, найкраще джерело інформації — [документація Microsoft на Microsoft Learn](https://learn.microsoft.com/). У цьому завданні вам потрібно прочитати документацію про прив'язки Azure Functions і з'ясувати, як налаштувати вихідну прив'язку.

Ось кілька сторінок, з яких варто почати:

* [Концепції тригерів і прив'язок Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-triggers-bindings?tabs=python)
* [Огляд прив'язок Azure Blob Storage для Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-bindings-storage-blob)
* [Вихідна прив'язка Azure Blob Storage для Azure Functions](https://learn.microsoft.com/azure/azure-functions/functions-bindings-storage-blob-output?tabs=python)

## Критерії оцінювання

| Критерій | Відмінно | Достатньо | Потребує покращення |
| -------- | --------- | -------- | ----------------- |
| Налаштування вихідної прив'язки до blob-сховища | Налаштовує вихідну прив'язку, повертає блоб, і він успішно зберігається в blob-сховищі | Налаштовує вихідну прив'язку або повертає блоб, але його не вдається зберегти в blob-сховищі | Не може налаштувати вихідну прив'язку |
