import logging
import re
import sys
from typing import Literal

from pandas import DataFrame, ExcelFile, read_excel

import config


# FIXME Переписать в чистовик
class TB1(object):

    def __init__(self) -> None:
        self.__filename: str
        self.__sheet_names: list[int | str]
        self.__sheets: dict


    def read(self, filename: str) -> bool:
        try:
            self.__filename = filename
            self.__sheet_names = ExcelFile(self.__filename).sheet_names
            # self.__sheets = {content: self.__read_sheet(content) for content in ('Ai', 'Di', 'Do')}
            self.__sheets = {'Ai': self.__read_sheet('Ai')} # FIXME Чтение только одного листа для тестов

            # TODO Придумай проверку
            return True if self.__sheets else False

        except Exception as error:
            logging.error(f'Не удалость прочитать файл - {error}')
            sys.exit(1)


    def __search_sheet(self, names_list: list, content_type: Literal['Ai', 'Di', 'Do']) -> str | None:
        'Return name of the sheet by content type'
        #TODO Валидатор
        #TODO Логи

        for name in names_list:
            match = re.fullmatch(config.TB1[f'{content_type}']['regex']['sheet']['validate']['name'], name)
            if match:
                return match.string
        return None


    def __get_columns_range(self, header_rows: tuple, content_type: Literal['Ai', 'Di', 'Do']): # TODO Отрефакторить бардак
        conf = config.TB1[f'{content_type}']['regex']['columns']
        required_columns: dict = conf['validate']['names']
        output_range = []
        output_col_names = []
        for row in header_rows:
            for cell_index, cell_value in enumerate(row):
                if not isinstance(cell_value, str): continue
                for required_col_name in required_columns:
                    replace_conf = conf['replace']['trash']
                    clear_cell_value = re.sub(replace_conf['pattern'], replace_conf['new_value'], cell_value)
                    match = re.fullmatch(required_columns[required_col_name], clear_cell_value)
                    if match:
                        output_range.append(cell_index)
                        output_col_names.append(required_col_name)
        if len(required_columns) != len(output_range):
            raise ValueError('Это жопа!')
        return ','.join(chr(i + 97) for i in output_range).upper(), output_col_names



    def __read_sheet(self, content_type: Literal['Ai', 'Di', 'Do'], ignore_trash=True) -> DataFrame | None:
        logging.info(f'Чтение листа {content_type}..')
        try:
            # Получение валидного названия листа
            valid_sheet_name = self.__search_sheet(self.__sheet_names, content_type)

            if not valid_sheet_name:
                return None

            # Поиск первой строки с контентом и индексов нужных столбцов
            test_df: DataFrame = read_excel(self.__filename, valid_sheet_name, header=None, nrows=10)
            first_col_content: list = test_df.iloc[:, 0].tolist()
            for i, row in enumerate(first_col_content):
                if content_type.upper() in str(row):
                    start_index: int = i
                    break
            

            header_rows = list(test_df.loc[row_index].tolist() for row_index in range(start_index))
            # Чтение
            columns = self.__get_columns_range(header_rows, content_type)
            sheet: DataFrame = read_excel(
                self.__filename,
                valid_sheet_name,
                header = None,
                skiprows = range(0, start_index),
                usecols = columns[0]
            )
            
            if not ignore_trash:
                return sheet
            else:
                # Переименование колонок
                sheet = sheet.rename(columns=dict(zip(list(sheet), columns[1])))
                # Очистка листа от мусора
                sheet = sheet.loc[sheet['name'] != 'Резерв'].dropna(axis=0, how='all').reset_index()
                del sheet['index']
                normalize = list(config.TB1[f'{content_type}']['regex']['columns']['validate']['names'])
                sheet = sheet[normalize]
                return sheet
                
        except Exception as error:
            logging.error(f'Ошибка чтения листа - {valid_sheet_name}: {error}')
            return None
        

    def get(self, content_type: Literal['Ai', 'Di', 'Do']) -> DataFrame | None:
        "Getting sheet's dataframe from TB1"
        return self.__sheets.get(content_type)
