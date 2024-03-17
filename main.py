import logging
import os
import sys

import pandas

from src.report.report import Report
from src.report.sheet_maker import ReportSheetMaker
from src.tb1.parser import TB1Parser
from src.tb1.tb1 import TB1


# Настройка логера
logging.basicConfig(level=logging.DEBUG)
# logging.basicConfig(level=logging.ERROR)

# Настройка полного вывода таблицы
pandas.set_option("display.max_rows", None)
pandas.set_option('display.max_colwidth', None)


def main():
    
    # Поиск эксельки
    logging.info('Поиск эксель-файла в директории...')
    valid_files = [filename for filename in os.listdir('temp') if filename.endswith(('xlsx', 'xls'))]

    if len(valid_files) == 1:
        tb1_filename = f'temp/{valid_files[0]}'
        logging.info(f'Найден файл - {tb1_filename}')
    else:
        logging.error('Неподдерживаемый формат или неверное количество эксель-файлов в директории')
        sys.exit(1)
    
    # Попытка создания объекта из файла
    try:
        tb1 = TB1()
        parser = TB1Parser()
        report_sheet_maker = ReportSheetMaker()
        report = Report()
        if tb1.read(tb1_filename):
            # TODO
            Ai_sheet = tb1.Ai_sheet
            # Di_sheet = tb1.get('Di')
            print(Ai_sheet, end='\n\n')
            # print(Di_sheet)
            # Ai_signals = parser.get_Ai_signal_list(Ai_sheet)
            # print(Ai_signals)
            # report_sheet = report_sheet_maker.get_empty(Ai_signals)
            # print(report_sheet)
            # report.add_sheet(report_sheet)
            # report_sheet.to_excel('temp/test.xlsx', index=False)
            # print(report_sheet)
        else:
            logging.error('Прекращение работы программы по причине ошибки чтения файла..')
            sys.exit(1)
    except Exception as error:
        logging.error(error)
        pass


if __name__ == "__main__":
    main()