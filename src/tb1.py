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
        # Получение валидного названия листа
        valid_sheet_name = TB1Helper.search_sheet(self.__sheet_names, content)

        if not valid_sheet_name:
            return None
        
        try:
            # Поиск первой строки с контентом
            first_col_content: list = read_excel(self.__filename, valid_sheet_name, header=None, nrows=10).iloc[:, 0].tolist()
            for i, row in enumerate(first_col_content):
                if content.upper() in str(row):
                    start_index: int = i
                    break
                
            # Чтение
            sheet: DataFrame = read_excel(
                self.__filename,
                valid_sheet_name,
                header=None,
                skiprows=range(0, start_index),
                usecols=','.join(config.TB1[f'{content}_SHEET']['columns'].values())
            )

            if not ignore_trash:
                return sheet
            else:
                # Очистка листа от мусора
                sheet = sheet.loc[sheet[list(sheet)[1]] != 'Резерв'].dropna(axis=0, how='all').reset_index()
                del sheet['index']
                # Переименование колонок
                sheet = sheet.rename(columns=dict(zip(list(sheet), list(config.TB1[f'{content}_SHEET']['columns']))))
                return sheet
                
        except Exception as error:
            logging.error(f'Ошибка чтения листа - {valid_sheet_name}: {error}')
            return None
        

    def get(self, content: Literal['Ai', 'Di', 'Do']) -> DataFrame | None:
        return self.__sheets.get(content)