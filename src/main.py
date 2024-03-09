import logging
import os
import sys

import pandas

from testing_assistant.report.sheet_maker import ReportSheetMaker
from testing_assistant.tb1.parser import TB1Parser
from testing_assistant.tb1.tb1 import TB1


# Настройка логера
logging.basicConfig(level=logging.DEBUG)

# Настройка полного вывода таблицы
pandas.set_option("display.max_rows", None)


def main():
    
    # Поиск эксельки
    logging.info('Поиск эксель-файла в директории...')
    valid_files = [filename for filename in os.listdir('temp') if filename.endswith(('xlsx', 'xls'))]
    print(valid_files)

    if len(valid_files) == 1:
        tb1_filename = f'temp/{valid_files[0]}'
        logging.info(f'Найден файл - {tb1_filename}')
    else:
        logging.error('Неподдерживаемый формат или неверное количество эксель-файлов в директории')
        sys.exit(1)
    
    # Попытка создания объекта из файла
    logging.info('Чтение файла..')
    try:
        tb1 = TB1()
        parser = TB1Parser()
        reporter = ReportSheetMaker()
        if tb1.read(tb1_filename):
            # TODO
            Ai_sheet = tb1.get('Ai')
            lst = parser.get_Ai_storage(Ai_sheet)
            print(reporter.get_empty(lst))
        else:
            logging.error('Прекращение работы программы по причине ошибки чтения файла..')
            sys.exit(1)
    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main()