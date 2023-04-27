## Тестовое задание Python
Представьте, что у вас есть система без интерфейса пользователя, например crawler (сборщик 
информации), который парсит все сайты по продаже зюзюбликов и сохраняет в базу данных.
Появилась потребность дать обычному пользователю минимальными усилиями добавлять еще 
сайты для парсинга
Напишите простого бота, который будет иметь одну кнопку: загрузить файл
1. При нажатии кнопки пользователь прикрепляет файл excel в формате таблицы с 
полями:
a. title - название
b. url - ссылка на сайт источник
c. xpath - путь к элементу с ценой
2. Бот получает файл, сохраняет
3. Открывает файл библиотекой pandas
4. Выводит содержимое в ответ пользователю
5. Сохраняет содержимое в локальную БД sqlite
Реализация на python, решение должно быть представлено ссылкой на репозиторий и на бота 
(как основной вариант telegram, но возможно вы предложите что-то еще).
Учесть возможность того, что сумма будет с пробелами, обозначением валюты и прочее.
Внутри репозитория должна быть инструкция по развёртыванию и корректный файл с 
необходимыми зависимостями (requirements, pipenv, poetry на ваш выбор)
Задание рассчитано на один день, выполнять можно в удобное время в течение недели
Задача со звездочкой:
Провести парсинг по данным из таблицы и вывести среднюю цену зюзюблика по каждому 
сайту,
В качестве зюзюблика можете взять любой интересный вам товар.

```

### Запуск проекта
Клонируем репозиторий и переходим в него:
```bash
git clone https://github.com/ilin-art/test_Technesis
cd test_Technesis
```
#### Создаем и активируем виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```
#### для Windows
```bash
python -m venv venv
source venv/Scripts/activate
```

#### Обновиляем pip и ставим зависимости из requirements.txt:
```bash
python -m pip install --upgrade pip && pip install -r requirements.txt
```
#### Запишете токен в общее пространство переменных окружения:
```bash
export TOKEN='token'
```
#### Запускаем проект:
```bash
python main.py
```