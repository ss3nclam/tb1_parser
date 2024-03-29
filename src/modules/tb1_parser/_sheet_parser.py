import logging
import re

from pandas import DataFrame
from transliterate import translit


class SheetParser:

    def __init__(self, sheet: DataFrame) -> None:
        self._logs_owner: str = self.__class__.__name__
        self._sheet = sheet

        self._result = None


    # REFACT Отрефакторить метод очистки имени сигнала
    def _clean_name(self):
        pass


    # REFACT Отрефакторить метод поиска количества каналов для модуля
    def _find_count_plc_channels(self, raw_plc_module: str):
        try:
            sheet: DataFrame = self._sheet
            count: int = len(sheet[sheet['plc_module'] == raw_plc_module])
            return count
        except Exception as exception:
            pass
        finally:
            pass


    # REFACT Переписать метод для парсинга переменной сигнала
    def _parse_variable(self, raw_variable: str, raw_plc_module: str) -> int | tuple[int]:
        type_regex = r'^\D{2}'
        clean_input = lambda x: re.sub(type_regex, '', x)
        clear_variable = clean_input(raw_variable)
        try:
            if 'ai' in raw_variable.lower():
                out = int(clear_variable)
            else:
                out = nums = tuple(map(int, clear_variable.split('-')))
        except ValueError as value_error:
            logging.warning(f'{self._logs_owner}: некорректный номер переменной "{raw_variable}"')
            count_plc_channels = self._find_count_plc_channels(raw_plc_module)
            nums = tuple(map(int, clear_variable.split('-')))
            if len(nums) == 2:
                logging.info(f'{self._logs_owner}: вычисление порядкового номера "{raw_variable}"')
                out = count_plc_channels * nums[0] + nums[1]
                logging.warning(f'{self._logs_owner}: номер переменной "{raw_variable}" принудительно нормализован - "{out}"')
            else:
                raise ValueError('попытка вычисления порядкового номера переменной провалена')
        except Exception as exception:
            logging.error(f'{self._logs_owner}: ошибка парсинга "{raw_variable}" переменной - {type(exception).__name__}:{exception}')
            out = None
        finally:
            return out


    # REFACT Перенести регулярку для транслитерации имени в либу
    replace_data = {
        r'\((\w+\b\s?){4,}\)': '',
        r'[\.\(\)\=\%\>\<\\\|\/\№\≤\≥\"\']': '',
        r'[Тт]очк\w+\b\s': 'т',
        r'[Гг]рупп\w+\b\s': 'г',
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
        'Вибрация': 'Вибр',
        'Виброперемещение': 'Вибр',
        'Виброскорость': 'Вибр'
    }

    
    # REFACT Переписать метод транслитерациии названия параметра
    def _format_signal_name(self, name: str) -> str:
        try:
            for key, value in self.replace_data.items():
                name = re.sub(key, value, name)
            name = translit(name, 'ru', reversed=True)
            name = re.split(r'\s+|\-|\,', name)
            name = (word for word in name if word != '')
            name = '_'.join(name).replace('\'', '')
            out: str = name
        except Exception as error:
            logging.error(f'{self._logs_owner}: ошибка транслитерации "{name}" названия параметра - {error}')
            out = None
        finally:
            return out
    

    # REFACT Переписать метод парсинга канала модуля плк
    def _parse_plc_module(self, raw_string: str) -> str:
        try:
            out = re.findall(r'^\w{2}\-[a-z0-9-]+\,?\s+?\(?(\w(\d+).?(\d+))\)?$', raw_string)[0][1:] # REFACT Перенести регулярку для модуля плк в либу
            out = tuple(map(int, out))
            if not out:
                raise ValueError('ошибка сопоставления с шаблоном')
        except Exception as error:
            logging.error(f'{self._logs_owner}: ошибка парсинга "{raw_string.replace('\n', '')}" модуля плк - {error}')
            out = None
        finally:
            return out
