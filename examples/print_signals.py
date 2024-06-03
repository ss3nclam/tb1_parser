import re

from tb1_parser import ParsedTB1Collection, TB1Parser

tb1 = TB1Parser("temp/table.xlsx")
tb1.read()

signals: ParsedTB1Collection = tb1.collection

my_filters = {
    "Температурные": lambda x: re.search(r"[Тт]емп", x.name),
    "Сигналы с защитой": lambda x: x.isprotected(),
    "Резервные": lambda x: not x.isused(),
    "Резервные": 12
}

for name, filter in my_filters.items():
    if filtered_signals := signals.filter(key=filter):
        print(f"\n{name} ({filtered_signals.count}):\n" + str(filtered_signals))
