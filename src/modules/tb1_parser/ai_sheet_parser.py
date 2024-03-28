import logging
import re

from pandas import DataFrame
from transliterate import translit

from src.modules.regex_lib import TB1 as config
from src.modules.types.ai_signal import AiSignal
from src.modules.types.ai_signals_collection import AiSignalsCollection


class AiSheetParser:

    def __init__(self, sheet: DataFrame) -> None:
        self.__logs_owner: str = self.__class__.__name__
        self.__sheet = sheet

        self.__result = None


    # REFACT Отрефакторить метод поиска количества каналов для модуля
    def __find_count_plc_channels(self, raw_plc_module: str):
        try:
            sheet: DataFrame = self.__sheet
            count: int = len(sheet[sheet['plc_module'] == raw_plc_module])
            return count
        except Exception as exception:
            pass
        finally:
            pass


    # TODO Написать метод для парсинга переменной сигнала
    def __parse_variable(self, raw_variable: str, raw_plc_module: str) -> int:
        clean_input = lambda x: re.sub(r'^\D{2}', '', x)
        clear_variable = clean_input(raw_variable)
        try:
            out = int(clear_variable)
        except ValueError as value_error:
            logging.warning(f'{self.__logs_owner}: некорректный номер переменной "{raw_variable}"')
            count_plc_channels = self.__find_count_plc_channels(raw_plc_module)
            nums = tuple(map(int, clear_variable.split('-')))
            if len(nums) == 2:
                logging.info(f'{self.__logs_owner}: вычисление порядкового номера "{raw_variable}"')
                out = count_plc_channels * nums[0] + nums[1]
                logging.warning(f'{self.__logs_owner}: номер переменной "{raw_variable}" принудительно нормализован - "{out}"')
            else:
                raise ValueError('попытка вычисления порядкового номера переменной провалена')
        except Exception as exception:
            logging.error(f'{self.__logs_owner}: ошибка парсинга "{raw_variable}" переменной - {type(exception).__name__}:{exception}')
            out = None
        finally:
            return out


    replace_data = { # REFACT Перенести регулярку для транслитерации имени в либу
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

    
    # REFACT Переписать метод транслитерациия названия параметра
    def __format_signal_name(self, name: str) -> str:
        try:
            for key, value in self.replace_data.items():
                name = re.sub(key, value, name)
            name = translit(name, 'ru', reversed=True)
            name = re.split(r'\s+|\-', name)
            name = (word for word in name if word != '')
            name = '_'.join(name).replace('\'', '')
            out: str = name
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка транслитерации "{name}" названия параметра - {error}')
            out = None
        finally:
            return out
    

    # REFACT Переписать метод парсинга канала модуля плк
    def __parse_plc_module(self, raw_string: str) -> str:
        try:
            out = re.findall(r'^\w{2}\-[a-z0-9]+\,?\s?\(?(\w(\d+).?(\d+))\)?', raw_string)[0][1:] # REFACT Перенести регулярку для модуля плк в либу
            out = tuple(map(int, out))
            if not out:
                raise ValueError('ошибка сопоставления с шаблоном')
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка парсинга "{raw_string.replace('\n', '')}" модуля плк - {error}')
            out = None
        finally:
            return out


    # REFACT Переписать метод парсинга единицы измерения из диапазона
    def __find_unit(self, range: str) -> str:
        out = None
        try:
            if (unit := range.split(' ')[-1]) and unit != 'нет':
                out = unit
                out = re.sub(r'\d+', '', out)
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка поиска единицы измерения в "{range}" диапазоне измерения - {error}')
        finally:
            return out


    # REFACT Отрефакторить метод парсинга диапазонов
    def __parse_range(self, raw_range: str | None) -> list:
        start = end = None
        try:
            # Отсев пустого диапазона
            if raw_range is None or re.fullmatch(config['Ai']['regex']['content']['validate']['empty_range'], raw_range):
                return start, end
            
            else:
                # Очистка инпута от мусора
                replace_methods: dict = config['Ai']['regex']['content']['replace']
                for method in replace_methods:
                    method_data: dict = replace_methods.get(method)
                    pattern, new_value = (i for i in method_data.values())
                    raw_range = re.sub(pattern, new_value, raw_range)

                # Если диапазон простой
                simple_range_regex = r'^(([0-9]+[.,])?[0-9]+)\s?\-\s?(([0-9]+[.,])?[0-9]+)(\s?\D+)?$' # REFACT Перенести регулярку парсинга простого диапазона в либу
                if re.fullmatch(simple_range_regex, raw_range):
                    simple_range = re.findall(simple_range_regex, raw_range)
                    start= simple_range[0][0]
                    end = simple_range[0][2]
                    # TODO Написать валидацию для простого диапазона

                else:
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
                        raise ValueError('некорректное число совпадений с шаблоном')

                # Финальное форматирование - конвертация в float
                format_func = \
                    lambda x: float(x.replace(',', '.')) if isinstance(x, str) else x
                out = [format_func(i) for i in (start, end)]

                # Если стартовое значение больше конечного
                if len(out) == 2 and None not in out:
                    if out[0] > out[1]:
                        logging.warning(f'{self.__logs_owner}: предупреждение при получении диапазона из "{raw_range}" - некорректно заполнено в ТБ1')
                        out = sorted(out)
                        logging.warning(f'{self.__logs_owner}: диапазон "{raw_range}" принудительно нормализован - {tuple(out)}')
                return out

        except Exception as exception:
            logging.error(f'{self.__logs_owner}: ошибка получения диапазона из "{raw_range}" - {exception}')
            return [*['parse_error']*2]

    
    def start(self) -> None:
        if not list(config['Ai']['regex']['columns']['validate']['names'].keys()) == list(self.__sheet):
            logging.error(f'{self.__logs_owner}: передан неверный лист аналоговых сигналов')

        out = []

        for row in self.__sheet.itertuples(False, 'Signal'):
            # logging.info(f'{self.__logs_owner}:{row.variable}: парсинг..')

            try:
                new = AiSignal()
                new.plc_module = self.__parse_plc_module(row.plc_module)
                new.variable = self.__parse_variable(row.variable, row.plc_module)
                
                new.name = row.name
                new.formated_name = self.__format_signal_name(row.name)
                new.unit = row.unit if row.unit else self.__find_unit(row.range)
                new.LL, new.HL = self.__parse_range(row.range)
                new.LW, new.HW = self.__parse_range(row.warning_range)
                new.LA, new.HA = self.__parse_range(row.alarm_range)
                new.LE, new.HE = self.__parse_range(row.error_range)

                out.append(new)
                logging.info(f'{self.__logs_owner}:{row.variable}: значения успешно получены')
            except Exception as error:
                logging.error(f'{self.__logs_owner}:{row.variable}: ошибка парсинга - {error}')
                out.append(new)
        self.__result = AiSignalsCollection(out)


    def get_result(self) -> AiSignalsCollection | None:
        if out := self.__result:
            return out
        else:
            logging.error(f'{self.__logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
            raise IndentationError