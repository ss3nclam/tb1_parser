import os

from tb1_parser import ParsedTB1Collection, TB1Parser

parser = TB1Parser("temp/table.xlsx")
parser.read()

tb1: ParsedTB1Collection = parser.collection


def print_signals(filtered_collection: ParsedTB1Collection):
    for signal_type, signals in filtered_collection.items():
        if len(signals):
            boarder: str = f" {signal_type} ".center(
                os.get_terminal_size().columns, "="
            )
            print(f"\n{boarder}\n")
            for signal in signals:
                print(signal)


my_filter = lambda signal: signal.isused() and signal.isprotected()

if filtered_signals := tb1.filter(key=my_filter):
    print_signals(filtered_signals)
