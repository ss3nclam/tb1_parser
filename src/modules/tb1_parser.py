import logging
import re
import sys

from pandas import DataFrame
from transliterate import translit, slugify

from src.modules.regex_lib import TB1 as config
from src.modules.types.signals import AiSignal

# from src.signals.ai_signal import AiSignal
# from src.signals.ai_signal_list import AiSignalList


#REFACT Пересобрать весь класс
class TB1Parser:

    def __init__(self) -> None:
        self.__logs_owner: str = self.__class__.__name__
    

    def __parse_range(self, raw_range: str, range_info: str='измерения') -> list[str]:
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


    def __parse_var(self):
        pass


    def __parse_plc_module(self):
        pass


    units_data = {
        'Температура': 'T',
        'Давление': 'P',
        'Перепад давления': 'dP',
        'Ток': 'I',
        'Напряжение': 'U',
        'Уровень': 'L',
        'Виброперемещение': 'Вибр',
        'Виброскорость': 'Вибр',
    }


    def __format_signal_name(self, name: str) -> str: # REFACT Переписать метод транслитерациия названия параметра
        name = re.sub(r'\((\w+\b\s?){4,}\)', '', name)
        name = re.sub(r'[\.\(\)]', '', name)
        name = re.sub(r'[Тт]очка\s', 'т', name)
        name = re.sub(r'[Оо]порн\w+\b\s[Пп]одш\w+\b', 'ОП', name)
        name = re.sub(r'[Оо]порн\w+\b\-[Уу]порн\w+\b\s[Пп]одш\w+\b', 'ОУП', name)
        name = re.sub(r'[Пп]одш\w+\b', 'подш', name)
        name = re.sub(r'([Пп]о\s)?[Оо]с[иь]\s?', '', name)
        for key, value in self.units_data.items():
            name = name.replace(key, value)
        name = translit(name, 'ru', reversed=True)
        name = re.split(r'\s+|\-', name)
        # print(name)
        name = (word for word in name if word != '')
        name = '_'.join(name).replace('\'', '')
        return name


    def get_Ai_signal_list(self, sheet: DataFrame) -> list:
        if not list(config['Ai']['regex']['columns']['validate']['names'].keys()) == list(sheet):
            logging.error('Парсер: передан неверный лист аналоговых сигналов')
            sys.exit(1)

        # out = AiSignalList()
        out = []

        for row in sheet.itertuples(False, 'Signal'):
            logging.info(f'{self.__logs_owner}:Ai: парсинг значений для "{row.name}"')

            new = AiSignal()
            new.variable = row.variable
            new.name = row.name

            try:
                new.formated_name = self.__format_signal_name(row.name)
                new.unit = row.unit # TODO Написать метод для парсинга единицы измерения из диапазона
                new.LL, new.HL = self.__parse_range(row.range)
                new.LW, new.HW = self.__parse_range(row.warning_range)
                new.LA, new.HA = self.__parse_range(row.alarm_range)
                new.LE, new.HE = self.__parse_range(row.error_range)
                new.plc_module = row.plc_module.replace('\n', ' ') # REFACT

                out.append(new)
            except Exception as error:
                logging.error(f'{self.__logs_owner}:Ai: ошибка парсинга "{row.name}" - {error}')
                out.append(new)
        return out
