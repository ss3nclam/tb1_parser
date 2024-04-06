import logging

import pandas

from src.modules.tb1_parser.tb1_parser import TB1Parser
from src.modules.tb1_parser.types._signal import Signal
from src.modules.tb1_parser.types.signals_collection import SignalsCollection
from src.modules.tb1_parser._tb1_file_reader import TB1FileReader
from src.modules.tb1_parser.types.tb1_readed_sheets_collection import \
    TB1ReadedSheetsCollection

# Настройка логера
logging.basicConfig(level=logging.DEBUG)

# Настройка полного вывода таблицы
pandas.set_option("display.max_rows", None)
pandas.set_option('display.max_colwidth', None)



reader = TB1FileReader(filepath='temp/table.xls')

reader.read()
tb1: TB1ReadedSheetsCollection = reader.sheets
for sheet_name, sheet_df in tb1.items():
    print(sheet_df)

parser = TB1Parser(tb1)
parser.read()

for name, collection in parser.collection.items():
    collection: SignalsCollection
    print(collection.signals_type)
    for element in collection:
        element: Signal
        if element.name != 'Резерв':
            print(element)
