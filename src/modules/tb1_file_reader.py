import logging
import re
import sys
from typing import Literal

from pandas import ExcelFile

from config import TB1 as config
from src.modules.types.tb1_sheets import TB1AiSheet, TB1DiSheet, TB1DoSheet


class TB1FileReader:

    def __init__(self, filepath: str) -> None:
        self.__logs_owner = self.__class__.__name__

        self.__filepath = filepath
        self.__file: ExcelFile | None = self.__read_file()
        self.__sheet_names: list[int | str] | None = self.__file.sheet_names

        self.__sheets: tuple | None = None


    def __read_file(self) -> ExcelFile | None:
        logging.info(f'{self.__logs_owner}: чтение файла "{self.__filepath}"..')
        try:
            logging.info(f'{self.__logs_owner}: успешно прочтён')
            excel_file = ExcelFile(self.__filepath)
            return excel_file
        except Exception:
            logging.error(f'{self.__logs_owner}: не удалось прочитать файл')
            sys.exit(1)


    def __find_sheet_name(self, content_type: Literal['Ai', 'Di', 'Do']) -> str | None:
        logging.info(f'{self.__logs_owner}: поиск названия листа "{content_type}"..')
        out: str | None = None
        try:
            for name in map(str, self.__sheet_names):
                match = re.fullmatch(config[f'{content_type}']['regex']['sheet']['validate']['name'], name)
                if match:
                    out = match.string
        except Exception:
            logging.error(f'{self.__logs_owner}: не удалось найти лист "{content_type}"')
        finally:
            return out


    def __get_columns_range(self):
        pass


    def __read_sheet(self):
        pass


    def read(self):
        logging.info(f'{self.__logs_owner}: начало чтения листов..')

    
    def test(self):
        return self.__file
