import logging
import re
from typing import Literal

from pandas import DataFrame, ExcelFile, read_excel

from src.modules.regex_lib import TB1 as config


class TB1SheetsReader:

    def __init__(self, file: ExcelFile) -> None:
        self.__logs_owner: str = self.__class__.__name__

        self.__file = file
    

    def __find_sheet_name(self, content_type: str) -> str | None:
        '''
        Приватный метод для поиска названия конкретного листа ТБ1.\n
        На входе принимает тип содержимого листа, если в либе с регулярками прописаны все его настройки.\n
        Примеры инпута: 'Ai', 'Di', 'Do'
        '''
        logging.info(f'{self.__logs_owner}: поиск листа "{content_type}"..')
        matches: list[str] = []
        try:
            for sheet_name in map(str, self.__file.sheet_names):
                name_pattern = config[f'{content_type}']['regex']['sheet']['validate']['name']
                if match := re.fullmatch(name_pattern, sheet_name):
                    matches.append(match.string)

            matches_count: int = len(matches)
            if matches_count == 1:
                out: str = matches[0]
                logging.info(f'{self.__logs_owner}: лист "{content_type}" успешно найден - "{out}"')
                return out
            else:
                raise ValueError(f'некорректное число совпадений с шаблоном ({matches_count})')
            
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка поиска листа "{content_type}" - {error}')
            return
    

    def __find_sheet_columns(self, content_type: str, df_header: list[list]) -> dict[str:int]: # REFACT Переписать метод поиска колонок
        '''
        Приватный метод для поиска индексов колонок конкреного листа ТБ1, перечисленных в либе регулярок.\n
        На входе тип содержимого листа и датафрейм из его шапки с названиями колонок.\n
        На выходе словарь с нормальизованными названиями колонок и их индексы.
        '''

        # TODO Логи
        # TODO Исключения

        columns_config = config[f'{content_type}']['regex']['columns']
        required_columns: dict = columns_config['validate']['names']
        replace_config = columns_config['replace']['trash']

        out: dict = {requared_column:None for requared_column in list(required_columns)}

        # Для строки в массиве из инпута
        for row in df_header:
            # Для ячейки в строке
            for cell_index, cell_value in enumerate(row):
                if not isinstance(cell_value, str): continue
                
                # Очистка содержимого ячейки от мусора
                clear_cell_value = re.sub(replace_config['pattern'], replace_config['new_value'], cell_value)
                
                # Для колонок из либы регулярок
                for requared_column, pattern in required_columns.items():
                    if re.fullmatch(pattern, clear_cell_value):
                        if out[requared_column] is None:
                            out[requared_column] = cell_index
        return out

    
    def read_sheet(self, content_type: str): # REFACT Переписать метод чтения листов
        # TODO Логи
        # TODO Исключения

        sheet_name = self.__find_sheet_name(content_type)

        if not sheet_name:
            return
        
        # Создание тестового фрейма
        test_df: DataFrame = read_excel(self.__file, sheet_name, header=None, nrows=10)
        # print(test_df)

        # Поиск первой строки с контентом и индексов нужных столбцов
        first_col_content: list = test_df.iloc[:, 0].tolist()
        for index, row in enumerate(first_col_content):
            if content_type.upper() in str(row):
                start_index: int = index
                break
        # print(start_index)
        header_rows = list(test_df.loc[row_index].tolist() for row_index in range(start_index))
        print(self.__find_sheet_columns(content_type, header_rows))