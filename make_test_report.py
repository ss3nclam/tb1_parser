import logging

import pandas

from src.modules.test_report_maker.temporary_report_maker import TemporaryReportMaker
from src.modules.tb1_parser.tb1_parser import TB1Parser
from src.modules.tb1_parser.types._signal import Signal
from src.modules.tb1_parser._tb1_file_reader import TB1FileReader
from src.modules.tb1_parser.types.tb1_readed_sheets_collection import \
    TB1ReadedSheetsCollection

# Настройка логера
logging.basicConfig(level=logging.DEBUG)

# Настройка полного вывода таблицы
pandas.set_option("display.max_rows", None)
pandas.set_option('display.max_colwidth', None)


# filename = 'table.xls'
# filename = 'table.xlsx'
filename = 'ЛДАР.421245.751_ТБ1.xlsx'
# filename = 'ЛДАР.421245.754 ТБ1.xlsx'
# filename = 'ЛДАР.421245.757 ТБ1.xlsx'

reader = TB1FileReader(filepath=f'temp/{filename}')
reader.read()
tb1: TB1ReadedSheetsCollection = reader.sheets
# for sheet_name, sheet_df in tb1.items():
#     print(sheet_df)

parser = TB1Parser(tb1)
parser.read()
signals_collection = parser.collection

for name, collection in parser.collection.items():
    print(collection.__class__.__name__)
    for element in collection:
        element: Signal
        if element.name != 'Резерв':
            print(element)

report_maker = TemporaryReportMaker(signals_collection)
report_maker.make()
report_maker.write(f'temp/{''.join(filename.split('.')[:-1])}_report.xlsx')