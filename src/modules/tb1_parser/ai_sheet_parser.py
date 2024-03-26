import logging
import re

from pandas import DataFrame
from transliterate import translit

from src.modules.regex_lib import TB1 as config
from src.modules.types.signals import AiSignal


class AiSheetParser:

    def __init__(self, sheet: DataFrame) -> None:
        self.__logs_owner: str = self.__class__.__name__
        self.__sheet = sheet

        self.__result = None


    # TODO Написать метод для парсинга переменной сигнала
    def __parse_variable(self):
        pass


    replace_data = {
        r'\((\w+\b\s?){4,}\)': '',
        r'[\.\(\)]': '',
        r'[Тт]очка\s': 'т',
        r'[Оо]порн\w+\b\s[Пп]одш\w+\b': 'ОП',
        r'[Оо]порн\w+\b\-[Уу]порн\w+\b\s[Пп]одш\w+\b': 'ОУП',
        r'[Пп]одш\w+\b': 'подш',
        r'([Пп]о\s)?[Оо]с[иь]\s?': '',
        'Температура': 'T',
        'Давление': 'P',
        'Перепад давления': 'dP',
        'Ток': 'I',
        'Напряжение': 'U',
        'Уровень': 'L',
        'Виброперемещение': 'Вибр',
        'Виброскорость': 'Вибр'
    }

    
    def __format_signal_name(self, name: str) -> str: # REFACT Переписать метод транслитерациия названия параметра
        for key, value in self.replace_data.items():
            name = re.sub(key, value, name)
        name = translit(name, 'ru', reversed=True)
        name = re.split(r'\s+|\-', name)
        # print(name)
        name = (word for word in name if word != '')
        name = '_'.join(name).replace('\'', '')
        return name
    

    # TODO Написать метод парсинга канала модуля плк
    def __parse_plc_module(self, raw_string: str) -> str:
        return raw_string.replace('\n', ' ')


    # TODO Написать метод парсинга единицы измерения из диапазона
    def __find_unit(self, range: str) -> str:
        return range.split(' ')[-1]


    # REFACT Отрефакторить метод парсинга диапазонов
    def __parse_range(self, raw_range: str) -> list[str]:
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
        
        # TODO Написать проверку ошибочного заполнения ТБ
        finally:
            final_format = lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x
            rng = (start, end)
            rng = rng if None in rng else sorted(rng)
            out = [final_format(i) for i in rng]
            # logging.info(f'Парсер: выходной диапазон - {out}')
            return out

    
    def start(self) -> tuple:
        if not list(config['Ai']['regex']['columns']['validate']['names'].keys()) == list(self.__sheet):
            logging.error(f'{self.__logs_owner}: передан неверный лист аналоговых сигналов')

        out = []

        for row in self.__sheet.itertuples(False, 'Signal'):
            logging.info(f'{self.__logs_owner}: парсинг значений для "{row.name}"')

            new = AiSignal()
            new.variable = row.variable
            new.name = row.name

            try:
                new.formated_name = self.__format_signal_name(row.name)
                new.plc_module = self.__parse_plc_module(row.plc_module)
                new.unit = row.unit if row.unit else self.__find_unit(row.range)
                new.LL, new.HL = self.__parse_range(row.range)
                new.LW, new.HW = self.__parse_range(row.warning_range)
                new.LA, new.HA = self.__parse_range(row.alarm_range)
                new.LE, new.HE = self.__parse_range(row.error_range)

                out.append(new)
            except Exception as error:
                logging.error(f'{self.__logs_owner}: ошибка парсинга "{row.name}" - {error}')
                out.append(new)
        self.__result = tuple(out)


    def get_result(self) -> tuple | None:
        if out := self.__result:
            return out
        else:
            logging.error(f'{self.__logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
            raise IndentationError