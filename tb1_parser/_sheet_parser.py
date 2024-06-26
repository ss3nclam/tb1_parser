import logging
import re

from pandas import DataFrame
from transliterate import translit

from ._regex_lib import PARSER as config
from .plc_module import PLCModule
from .signals_collection import SignalsCollection


class SheetParser:

    def __init__(self, sheet: DataFrame) -> None:
        self._logs_owner: str = self.__class__.__name__
        self._sheet = sheet

        self._result = None

    def _clean_name(self, raw_name: str) -> str:
        return raw_name.strip().replace('\n', '')

    def _parse_variable(self, raw_variable: str) -> str:
        return translit(raw_variable, 'ru', reversed=True)

    # REFACT Переписать метод транслитерациии названия параметра
    # def _format_signal_name(self, name: str) -> str:
    #     replace_data = config['signals']['format_variable_name']
    #     try:
    #         for key, value in replace_data.items():
    #             name = re.sub(key, value, name)
    #         name = translit(name, 'ru', reversed=True)
    #         name = re.split(r'\s+|\-|\,', name)
    #         name = (word for word in name if word != '')
    #         name = '_'.join(name).replace('\'', '')
    #         out: str = name
    #     except Exception as error:
    #         logging.error(f'{self._logs_owner}: ошибка транслитерации "{name}" названия параметра - {error}')
    #         out = None
    #     finally:
    #         return out
    
    def _parse_plc_module(self, raw_string: str) -> str:
        try:
            raw_string = translit(raw_string, 'ru', reversed=True)
            params = re.findall(config['signals']['find_plc_module'], raw_string)[0]

            if len(params) != 4:
                raise ValueError('ошибка сопоставления с шаблоном')
            
            out = PLCModule()
            out.type, out.module = params[::3]
            out.channels_count, out.some_num = map(int, params[1:3])
            
        except Exception as error:
            logging.error(f'{self._logs_owner}: ошибка парсинга "{raw_string.replace('\n', '')}" модуля плк - {error}')
            out = None

        finally:
            return out

    def _get_result(self) -> SignalsCollection | None:
        if out := self._result:
            return out
        else:
            logging.error(f'{self._logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
            raise IndentationError
