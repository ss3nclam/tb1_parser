from typing import Literal

from pandas import DataFrame, ExcelFile, read_excel

from config import config
from src.tb1_helper import TB1Helper
from src.tb1_sheet import TB1Sheet


class TB1():

    def __init__(self, tb1_file: ExcelFile) -> None:
        self.__file = tb1_file
        self.__sheets: dict[DataFrame] | None


    def __read_sheet(self, content: str, ignore_reserv=True) -> DataFrame | None:
        # Получение имени листа по его содержимому
        valid_sheet_name = TB1Helper.search_sheet(self.__file.sheet_names, content)

        # Чтение всего листа
        if valid_sheet_name:
            try:
                sheet: DataFrame = read_excel(
                    self.__file,
                    valid_sheet_name,
                    index_col=0,
                    usecols=config[f'{content}_SHEET']['columns_range'],
                    )
                return sheet.dropna(axis=0, how='all')
            except Exception as error:
                return
            
            # sheet.dropna(axis=0, how='all')
            
        # TODO Проверка на наличие шапки в листе
        # TODO Очистка листа от пустых строк и резервов
    
    
    def read(self) -> bool:
        try:
            self.__sheets = {
                content: TB1Sheet(
                    self.__read_sheet(content)) for content in ('Ai', 'Di', 'Do')
                }
            if len(self.__sheets.keys()) != 3:
                raise Exception
            return True
        except Exception as error:
            return False
    

    def get(self, content: Literal['Ai', 'Di', 'Do']) -> TB1Sheet:
        out: TB1Sheet = self.__sheets.get(content)
        return out.test()
        