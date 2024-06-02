import os

from tb1_parser import ParsedTB1Collection, TB1Parser

parser = TB1Parser('temp/table.xlsx')
parser.read()

my_filter = lambda signal: signal.isused() and signal.isprotected()

tb1: ParsedTB1Collection = parser.collection
filtered_collection = tb1.filter(key=my_filter)

for signal_type, signals in filtered_collection.items():
    if len(signals):
        boarder: str = f' {signal_type} '.center(os.get_terminal_size().columns, '=')
        print(f'\n{boarder}\n')
        for signal in signals:
            print(signal)
