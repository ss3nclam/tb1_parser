import logging
import sys
from typing import Literal

from pandas import DataFrame, ExcelFile, read_excel

import config
from src.tb1_helper import TB1Helper


class TB1(object):

    def __init__(self) -> None:
        self.__filename: str
        self.__sheet_names: list[int | str]
        self.__sheets: dict


    def read(self, filename: str) -> bool:
        try:
            self.__filename = filename
            self.__sheet_names = ExcelFile(self.__filename).sheet_names
            self.__sheets = {content: self.__read_sheet(content) for content in ('Ai', 'Di', 'Do')}

            return True if self.__sheets else False # TODO Придумай проверку

        except Exception as error:
            logging.error(f'Не удалость прочитать файл - {error}')
            sys.exit(1)


    def __read_sheet(self, content: Literal['Ai', 'Di', 'Do'], ignore_trash=True) -> DataFrame | None:
        # Получить валидное название листа
        valid_sheet_name = TB1Helper.search_sheet(self.__sheet_names, content)

        if not valid_sheet_name:
            return None
        
        try:
            read_sheet: DataFrame = lambda header: read_excel(
                self.__filename,
                valid_sheet_name,
                index_col=0,
                header=header,
                usecols=config.TB1[f'{content}_SHEET']['columns_range']
            )

            # Проверка на шапку в начале листа
            sheet: DataFrame = read_sheet(0)
            if list(sheet)[0] == 'Unnamed: 1':
                sheet = read_sheet(1)
            
            col_names = list(sheet)
            return sheet.loc[sheet[col_names[0]] != 'Резерв'].dropna(axis=0, how='all') if ignore_trash else sheet
        
        except Exception as error:
            logging.error(f'Ошибка чтения листа - {valid_sheet_name}: {error}')
            return None
        

    def get(self, content: Literal['Ai', 'Di', 'Do']) -> DataFrame | None:
        return self.__sheets.get(content)