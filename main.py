import os
import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import requests
import pandas as pd
import re
from lxml import etree
from db import save_to_sqlite


bot_token = os.getenv('TOKEN')
bot: telegram.Bot = telegram.Bot(token=bot_token)

def start_handler(update, context):
    """
    Обработчик команды /start
    """
    update.message.reply_text('Загрузите файл excel, чтобы добавить новые сайты для парсинга.')

def handle_file(update, context):
    """
    Обработчик загрузки файла пользователем
    """
    # Получить объект файла из сообщения пользователя
    file = context.bot.get_file(update.message.document.file_id)
    file_name = file.file_path.split("/")[-1]

    # Скачать файл и сохранить его в папку downloads
    file_path = f"{os.getcwd()}/downloads/{file_name}"
    file.download(file_path)

    # Проверить, что файл Excel содержит все необходимые колонки
    try:
        with pd.ExcelFile(file_path) as xls:
            sheet_names = xls.sheet_names
            if 'Sheet1' in sheet_names or 'Лист1' in sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_names[0])
                if set(['title', 'url', 'xpath']).issubset(df.columns):
                    titles, urls, xpaths, prices = parse_excel_file(file_path)

                    # Отправить пользователю сообщение о данных из таблицы Excel
                    message = f"Вы загрузили данные из таблицы Excel со следующими значениями:\n\n"
                    for i in range(len(titles)):
                        message += f"Заголовок: {titles[i]}\n"
                        message += f"URL: {urls[i]}\n"
                        message += f"XPath: {xpaths[i]}\n"
                        message += f"Средняя стоимость: {prices[i]}\n"
                        message += "\n"
                    update.message.reply_text(message)

                    # Сохранить данные в базу данных sqlite
                    save_to_sqlite(file_path)

                    # Отправить пользователю сообщение об успешной загрузке
                    update.message.reply_text('Файл успешно загружен и сохранен в базу данных!')
                else:
                    update.message.reply_text('Ошибка! Файл Excel не содержит необходимые колонки (title, url, xpath)')
            else:
                update.message.reply_text('Ошибка! Файл Excel должен иметь хотя бы одну страницу с названием "Sheet1"')
    except Exception as e:
        update.message.reply_text('Ошибка! Невозможно обработать файл Excel. Попробуйте загрузить другой файл.')
        print(str(e))


def parse_sites_price(urls: list[str], xpaths: list[str]) -> list[float]:
    """
    Функция парсинга цен на сайтах
    """
    # Создание списка для хранения средних цен на сайтах
    prices = []

    # Цикл по списку ссылок и путей к ценам на сайтах
    for url, xpath in zip(urls, xpaths):
        try:
            # Запрос страницы сайта
            response = requests.get(url)
            response.encoding = response.apparent_encoding

            # Получение содержимого страницы
            html = response.text
            # Создание парсера для HTML
            parser = etree.HTMLParser()

            # Парсинг содержимого страницы
            tree = etree.fromstring(html, parser)

            # Парсинг цены с помощью XPath
            price_list = []
            for element in tree.xpath(xpath):
                price = element.text.strip()
                if price:
                    # Убираем пробелы, запятые и прочие символы из цены
                    price = re.sub(r'[^\d.,]+', '', price)
                    # Заменяем запятую на точку
                    price = price.replace(',', '.')
                    # Конвертируем цену в число
                    price = float(price)
                    price_list.append(price)
            
            # Вычисление средней цены
            if len(price_list) > 0:
                average_price = sum(price_list) / len(price_list)
                average_price = round(average_price, 2)
            else:
                average_price = 'Цена не найдена'
        except requests.exceptions.RequestException:
            average_price = 'Ошибка при получении цены: не удалось выполнить запрос на сайт'
        except ValueError:
            average_price = 'Ошибка при получении цены: неверный формат цены'
        except Exception:
            average_price = 'Ошибка при получении цены: неизвестная ошибка'

        prices.append(average_price)

    return prices

def parse_excel_file(file_path: str) -> tuple[list[str], list[str], list[str], list[float]]:
    # Чтение файла Excel с помощью библиотеки pandas
    file_read = pd.read_excel(file_path)
    
    # Получение необходимых данных из таблицы
    titles = file_read['title'].tolist()
    urls = file_read['url'].tolist()
    xpaths = file_read['xpath'].tolist()
    prices = parse_sites_price(urls, xpaths)
    
    return titles, urls, xpaths, prices


# Создаем объект updater и dispatcher
updater = Updater(bot_token)
dispatcher = updater.dispatcher

# Регистрируем обработчики команд и сообщений
dispatcher.add_handler(CommandHandler('start', start_handler))
dispatcher.add_handler(MessageHandler(Filters.document, handle_file))

# Запускаем бота
updater.start_polling()
updater.idle()
