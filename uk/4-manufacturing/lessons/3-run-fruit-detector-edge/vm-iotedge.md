# Створіть віртуальну машину з IoT Edge

> 👩‍🏫 Цю частину показує викладач (демо). Віртуальна машина платна, тому після демонстрації обов'язково видаліть її.

В Azure можна створити віртуальну машину — комп'ютер у хмарі, який можна налаштувати як завгодно й запускати на ньому власне програмне забезпечення.

> 💁 Більше про віртуальні машини можна прочитати на [сторінці Virtual machine у Вікіпедії](https://wikipedia.org/wiki/Virtual_machine) (англійською).

## Завдання: налаштуйте віртуальну машину з IoT Edge

1. Виконайте таку команду, щоб створити VM із попередньо встановленим Azure IoT Edge:

    ```sh
    az deployment group create \
                --resource-group fruit-quality-detector \
                --template-uri https://raw.githubusercontent.com/Azure/iotedge-vm-deploy/main/edgeDeploy.json \
                --parameters dnsLabelPrefix=<vm_name> \
                --parameters adminUsername=<username> \
                --parameters deviceConnectionString="<connection_string>" \
                --parameters authenticationType=password \
                --parameters adminPasswordOrKey="<password>"
    ```

    Замініть `<vm_name>` на назву цієї віртуальної машини. Вона має бути глобально унікальною, тож використайте щось на кшталт `fruit-quality-detector-vm-` з вашим ім'ям чи іншим значенням у кінці.

    Замініть `<username>` і `<password>` на ім'я користувача й пароль для входу у VM. Вони мають бути достатньо надійними, тож admin/password не підійдуть.

    Замініть `<connection_string>` на рядок підключення свого пристрою IoT Edge `fruit-quality-detector-edge`.

    Ця команда створить VM конфігурації `DS1 v2`. Ці категорії вказують, наскільки потужна машина і, відповідно, скільки вона коштує. Ця VM має 1 CPU і 3,5 ГБ оперативної пам'яті.

    > 👩‍🏫 **Примітка до цієї версії.** В оригіналі використовувався шаблон `iotedge-vm-deploy/1.2.0`, що встановлює застарілу версію IoT Edge. Шаблон із гілки `main` встановлює IoT Edge 1.6 на Ubuntu 22.04.

    > 💰 Актуальні ціни на ці VM можна подивитися на [сторінці цін на віртуальні машини Azure](https://azure.microsoft.com/pricing/details/virtual-machines/linux/).

    Після створення VM середовище виконання IoT Edge встановиться автоматично й буде налаштоване на підключення до вашого IoT Hub як пристрій `fruit-quality-detector-edge`.

1. Щоб викликати класифікатор зображень на VM, знадобиться її IP-адреса або DNS-ім'я. Отримайте їх такою командою:

    ```sh
    az vm list --resource-group fruit-quality-detector \
               --output table \
               --show-details
    ```

    Скопіюйте значення поля `PublicIps` або поля `Fqdns`.

1. VM коштують грошей. На момент написання оригінального уроку VM DS1 коштувала близько $0,06 на годину. Щоб зменшити витрати, вимикайте VM, коли не користуєтеся нею, і видаліть її, коли закінчите цей проєкт.

    Можна налаштувати VM на автоматичне вимкнення щодня в певний час. Тоді, якщо ви забудете її вимкнути, вам не виставлять рахунок більше ніж до часу автоматичного вимкнення. Налаштуйте це такою командою:

    ```sh
    az vm auto-shutdown --resource-group fruit-quality-detector \
                        --name <vm_name> \
                        --time <shutdown_time_utc>
    ```

    Замініть `<vm_name>` на назву своєї віртуальної машини.

    Замініть `<shutdown_time_utc>` на час за UTC, коли VM має вимикатися, у форматі з 4 цифр ГГХХ. Наприклад, щоб вимикати опівночі за UTC, укажіть `0000`. Для 19:30 за київським часом укажіть `1730` взимку (UTC+2) або `1630` влітку (UTC+3).

1. Ваш класифікатор зображень працюватиме на цьому периферійному пристрої й слухатиме порт 80 (стандартний порт HTTP). За замовчуванням у віртуальних машин вхідні порти заблоковано, тож порт 80 потрібно відкрити. Порти відкриваються в групах безпеки мережі (network security groups), тож спочатку дізнайтеся назву групи безпеки мережі своєї VM такою командою:

    ```sh
    az network nsg list --resource-group fruit-quality-detector \
                        --output table
    ```

    Скопіюйте значення поля `Name`.

1. Виконайте таку команду, щоб додати до групи безпеки мережі правило, яке відкриває порт 80:

    ```sh
    az network nsg rule create \
                        --resource-group fruit-quality-detector \
                        --name Port_80 \
                        --protocol tcp \
                        --priority 1010 \
                        --destination-port-range 80 \
                        --nsg-name <nsg name>
    ```

    Замініть `<nsg name>` на назву групи безпеки мережі з попереднього кроку.

### Завдання: керуйте VM, щоб зменшити витрати

1. Коли VM не використовується, її слід вимикати. Щоб вимкнути VM, виконайте таку команду:

    ```sh
    az vm deallocate --resource-group fruit-quality-detector \
                     --name <vm_name>
    ```

    Замініть `<vm_name>` на назву своєї віртуальної машини.

    > 💁 Є команда `az vm stop`, яка зупиняє VM, але залишає комп'ютер закріпленим за вами, тож ви й далі платите так, ніби він працює.

1. Щоб знову запустити VM, виконайте таку команду:

    ```sh
    az vm start --resource-group fruit-quality-detector \
                --name <vm_name>
    ```

    Замініть `<vm_name>` на назву своєї віртуальної машини.
