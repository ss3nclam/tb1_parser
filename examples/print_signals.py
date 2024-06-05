import re
from pprint import pprint

from tb1_parser import ParsedTB1Collection, TB1Parser

tb1 = TB1Parser("temp/table.xlsx")
tb1.read()

tb1_collection: ParsedTB1Collection = tb1.collection

my_filters = {
    "Температурные": lambda x: re.search(r"[Тт]емп", x.name),
    "Сигналы с защитой": lambda x: x.isprotected(),
    "Резервные": lambda x: not x.isused(),
}

for name, filter in my_filters.items():
    if filtered_signals := tb1_collection.filter(key=filter):
        print(f"\n{name}:")
        pprint(filtered_signals)
