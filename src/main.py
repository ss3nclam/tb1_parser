import logging
import os
import sys

import pandas


# Настройка логера
logging.basicConfig(level=logging.DEBUG)

# Настройка полного вывода таблицы
pandas.set_option("display.max_rows", None)


def main():
    
    # Поиск эксельки
    logging.info('Поиск эксель-файла в директории...')
    valid_files = [filename for filename in os.listdir() if filename.endswith(('xlsx', 'xls'))]

    if len(valid_files) == 1:
        tb1_filename = valid_files[0]
        logging.info(f'Найден файл - {tb1_filename}')
    else:
        logging.error('Неподдерживаемый формат или неверное количество эксель-файлов в директории')
        sys.exit(1)
    
    # Попытка создания объекта из файла
    logging.info(f'Чтение файла - {tb1_filename}')
    try:
        tb1 = TB1()
        if tb1.read(tb1_filename):
            pass
        else:
            logging.error('Ошибка чтения файла')
            sys.exit(1)
    except Exception as error:
        logging.error(error)