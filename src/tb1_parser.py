import logging
import re
import sys
from typing import Any

from pandas import DataFrame

import config
from src.Ai_signal import AiSignal


regex_main = r'((([Оо]т\s?)|([Дд]о\s?))?(([Мм]ен[а-я]+\s?)|([Бб]ол[а-я]+\s?)|[><])?((([Мм]ин([а-я]+\s?)?)|([Пп]л([а-я]+\s?)?)|[-+])\.?\s?)?([,.0-9]+))'


class TB1Parser:

    def __get_range(self, input: str) -> list[str]:
        try:
            input = str(input).replace('\n', '')
            if input in ('nan', 'нет'):
                start = None
                stop = None
            
            logging.info(f'Parser: поиск совпадений в "{input}"')
            matches_list: list[Any] = re.findall(regex_main, input)

            if not matches_list or len(matches_list) > 2:
                raise ValueError('некорректное количество совпадений')
            
            # for reg_groups in matches_list:
            #     match = reg_groups[0]
            
            start, stop = [i[0] for i in matches_list]
                
        except Exception as error:
            logging.error(f'Parser: не удалось распознать диапазон из "{input}" - {error}')
            start = 'parse_error'
            stop = 'parse_error'

        finally:
            return [start, stop]



    def get_Ai_signals(self, sheet: DataFrame) -> tuple[AiSignal]:
        'Getting Ai signals tuple'
        if not list(config.TB1['Ai_SHEET']['columns'].keys()) == list(sheet):
            logging.error('Parser: передан неверный лист аналоговых сигналов')
            sys.exit(1)

        out: list[AiSignal] = []

        for row in sheet.itertuples(False, 'Signal'):
            logging.info(f'Parser: получение значений для {row.name}')
            new = AiSignal()
            new.variable = row.variable
            new.name = row.name
            new.LL, new.HL = self.__get_range(row.range)
            new.LW, new.HW = self.__get_range(row.warning_range)
            new.LA, new.HA = self.__get_range(row.alarm_range)

            print(new)
            out.append(new)

        return tuple(out)
