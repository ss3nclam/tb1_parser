import os

from tb1_parser import Signal, TB1Parser

tb1 = TB1Parser('temp/table.xlsx')
tb1.read()

for key, signals_collection in tb1.collection.items():

    boarder: str = f' {key} '.center(os.get_terminal_size().columns, '=')
    print(f'\n{boarder}\n')

    for signal in signals_collection:
        signal: Signal
        
        if not signal.isreserv():
            print(signal)
