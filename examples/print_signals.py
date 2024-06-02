from re import search

from tb1_parser import ParsedTB1Collection, TB1Parser

parser = TB1Parser("temp/table.xlsx")
parser.read()

tb1: ParsedTB1Collection = parser.collection

my_filters = {
    "Резервные:": lambda x: not x.isused(),
    "Сигналы с защитой:": lambda x: x.isprotected(),
    "Температурные:": lambda x: search(r"[Тт]емп", x.name),
}

for name, filter in my_filters.items():
    if filtered_signals := tb1.filter(key=filter):
        print(f"\n{name}\n" + str(filtered_signals))
