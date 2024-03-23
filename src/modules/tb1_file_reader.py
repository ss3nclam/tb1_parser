import logging
import re
import sys
from typing import Literal

from pandas import ExcelFile

from config import TB1 as config
from src.modules.tb1_sheets_reader import TB1SheetsReader
from src.modules.types.tb1_sheets import TB1AiSheet, TB1DiSheet, TB1DoSheet


class TB1FileReader:

    def __init__(self, filepath: str) -> None:
        self.__logs_owner: str = self.__class__.__name__
        self.__filepath = filepath

        self.__sheets: tuple | None = None


    def __read_file(self) -> ExcelFile:
        logging.info(f'{self.__logs_owner}: открытие файла "{self.__filepath}"..')
        try:
            logging.info(f'{self.__logs_owner}: файл успешно открыт')
            excel_file = ExcelFile(self.__filepath)
            return excel_file
        except Exception:
            logging.error(f'{self.__logs_owner}: не удалось открыть файл')
            sys.exit(1)


    def read(self):
        logging.info(f'{self.__logs_owner}: начало чтения ТБ1..')
        sheet_reader = TB1SheetsReader(self.__read_file())
        sheet_reader.test()






    # def test(self):
    #     print(self.__sheet_names)
