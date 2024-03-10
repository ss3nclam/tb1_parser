import logging
import sys
from re import fullmatch
from typing import Literal

from pandas import DataFrame, ExcelFile, read_excel

import config as config


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


    def __search_sheet(self, names_list: list, content_type: Literal['Ai', 'Di', 'Do']) -> str | None:
        'Return name of the sheet by content type'
        #TODO Валидатор
        #TODO Логи

        reg = config.TB1[f'{content_type}_SHEET']['regex']['validate']['sheet_name']

        for name in names_list:
            match = fullmatch(reg, name)
            if match:
                return match.string
        return None


    def __read_sheet(self, content_type: Literal['Ai', 'Di', 'Do'], ignore_trash=True) -> DataFrame | None:
        logging.info(f'Чтение листа {content_type}..')
        try:
            # Получение валидного названия листа
            valid_sheet_name = self.__search_sheet(self.__sheet_names, content_type)

            if not valid_sheet_name:
                return None

            # Поиск первой строки с контентом
            first_col_content: list = read_excel(self.__filename, valid_sheet_name, header=None, nrows=10).iloc[:, 0].tolist()
            for i, row in enumerate(first_col_content):
                if content_type.upper() in str(row):
                    start_index: int = i
                    break
                
            # Чтение
            sheet: DataFrame = read_excel(
                self.__filename,
                valid_sheet_name,
                header=None,
                skiprows=range(0, start_index),
                usecols=','.join(config.TB1[f'{content_type}_SHEET']['columns'].values())
            )

            if not ignore_trash:
                return sheet
            else:
                # Переименование колонок
                sheet = sheet.rename(columns=dict(zip(list(sheet), list(config.TB1[f'{content_type}_SHEET']['columns']))))
                # Очистка листа от мусора
                sheet = sheet.loc[sheet['name'] != 'Резерв'].dropna(axis=0, how='all').reset_index()
                del sheet['index']
                return sheet
                
        except Exception as error:
            logging.error(f'Ошибка чтения листа - {valid_sheet_name}: {error}')
            return None
        

    def get(self, content_type: Literal['Ai', 'Di', 'Do']) -> DataFrame | None:
        "Getting sheet's dataframe from TB1"
        return self.__sheets.get(content_type)