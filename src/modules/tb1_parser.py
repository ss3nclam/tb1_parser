import logging
import re
import sys

from pandas import DataFrame

from src.modules.regex_lib import TB1 as config
from src.modules.types.signals import AiSignal

# from src.signals.ai_signal import AiSignal
# from src.signals.ai_signal_list import AiSignalList


#REFACT Пересобрать весь класс
class TB1Parser:

    def __parse_raw_Ai_range(self, raw_range: str, range_info: str='измерения') -> list[str]:
        start = end = None
        try:
            if re.fullmatch(config['Ai']['regex']['content']['validate']['empty_range'], raw_range):
                return start, end
            
            # logging.info(f'Парсер: получение диапазона {range_info} из "{raw_range}"..')
            # Очистка инпута от мусора
            replace_methods: dict = config['Ai']['regex']['content']['replace']
            for method in replace_methods:
                method_data: dict = replace_methods.get(method)
                pattern, new_value = (i for i in method_data.values())
                raw_range = re.sub(pattern, new_value, raw_range)
            # logging.info(f'Парсер: успешно - {raw_range}')

            # Поиск значений в очищеном инпуте
            matches_list = re.findall(config['Ai']['regex']['content']['validate']['range_value'], raw_range)
            matches_count = len(matches_list)

            if matches_count == 1:
                for match in matches_list:
                    if '<' in match[0]:
                        start = match[1]
                    elif '>' in match[0]:
                        end = match[1]
            elif matches_count == 2:
                start, end = [i[1] for i in matches_list]
            else:
                raise ValueError

        except ValueError:
            # logging.error(f'Парсер: ошибка получения диапазона из "{raw_range}"')
            start = end = 'parse_error'
        
        # REFACT Написать проверку ошибочного заполнения ТБ и отрефакторить
        finally:
            final_format = lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x
            rng = (start, end)
            rng = rng if None in rng else sorted(rng)
            out = [final_format(i) for i in rng]
            # logging.info(f'Парсер: выходной диапазон - {out}')
            return out


    def get_Ai_signal_list(self, sheet: DataFrame) -> list:
        if not list(config['Ai']['regex']['columns']['validate']['names'].keys()) == list(sheet):
            logging.error('Парсер: передан неверный лист аналоговых сигналов')
            sys.exit(1)

        # out = AiSignalList()
        out = []

        for row in sheet.itertuples(False, 'Signal'):
            logging.info(f'Парсер: получение значений для "{row.name}"')
            new = AiSignal()
            new.variable = row.variable
            new.name = row.name
            new.unit = row.unit
            new.LL, new.HL = self.__parse_raw_Ai_range(row.range)
            new.LW, new.HW = self.__parse_raw_Ai_range(row.warning_range)
            new.LA, new.HA = self.__parse_raw_Ai_range(row.alarm_range)
            new.plc_module = row.plc_module.replace('\n', ' ') # REFACT
            out.append(new)

        return out
