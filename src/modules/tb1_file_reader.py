import logging
import sys

from pandas import ExcelFile

from src.modules.regex_lib import TB1
from src.modules.tb1_sheets_reader import TB1SheetsReader


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
        sheets_reader = TB1SheetsReader(self.__read_file())
        sheets_reader.read_sheet('Ai')

        # requared_sheets = list(TB1)
        # if sheets_reader.read():
        #     for sheet_type in requared_sheets:
        #         self.__sheets[sheet_type] = sheets_reader.get(sheet_type)