import logging
import re
import sys

from pandas import DataFrame

import config as config
from testing_assistant.signals.ai_signal_list import AiSignalList
from testing_assistant.signals.ai_signal import AiSignal


class TB1Parser:

    def __parse_raw_Ai_range(self, input: str) -> list[str]:
        start = end = None

        try:
            if re.fullmatch(config.TB1['Ai_SHEET']['regex']['validate']['empty_range'], input):
                return start, end
            
            logging.info(f'Парсер: получение диапазона из "{input}"..')

            # Очистка инпута от мусора
            replace_methods: dict = config.TB1['Ai_SHEET']['regex']['replace']
            for method in replace_methods:
                method_data: dict = replace_methods.get(method)
                pattern, new_value = (i for i in method_data.values())
                input = re.sub(pattern, new_value, input)

            # Поиск значений в очищеном инпуте
            matches_list = re.findall(config.TB1['Ai_SHEET']['regex']['validate']['range_value'], input)
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
            logging.error(f'Парсер: ошибка получения диапазона из "{input}"')
            start = end = 'parse_error'
            
        finally:
            final_format = lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x
            return [final_format(i) for i in (start, end)]


    def get_Ai_signal_list(self, sheet: DataFrame) -> AiSignalList:
        if not list(config.TB1['Ai_SHEET']['columns'].keys()) == list(sheet):
            logging.error('Парсер: передан неверный лист аналоговых сигналов')
            sys.exit(1)

        out = AiSignalList()

        for row in sheet.itertuples(False, 'Signal'):
            logging.info(f'Парсер: получение значений для "{row.name}"')
            new = AiSignal()
            new.variable = row.variable
            new.name = row.name
            new.LL, new.HL = self.__parse_raw_Ai_range(row.range)
            new.LW, new.HW = self.__parse_raw_Ai_range(row.warning_range)
            new.LA, new.HA = self.__parse_raw_Ai_range(row.alarm_range)
            # print(new)
            out.append(new)

        return out
