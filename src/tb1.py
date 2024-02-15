from pandas import DataFrame, ExcelFile, read_excel

from src.tb1_helper import TB1Helper
from src.tb1_sheet import TB1Sheet


class TB1():

    def __init__(self, tb1_file: ExcelFile) -> None:
        self.__file = tb1_file
        self.sheets: dict[DataFrame] | None


    def __read_sheet(self, content: str) -> DataFrame | None:
        # TODO Получение имени листа по его содержимому
        valid_sheet_name = TB1Helper.search_sheet(self.__file.sheet_names, content)

        if valid_sheet_name:
            try:
                sheet = read_excel(self.__file, valid_sheet_name)
                return sheet
            except Exception as error:
                return
            
    
    def read(self):
        self.sheets = {content: TB1Sheet(self.__read_sheet(content)) for content in ('Ai', 'Di', 'Do')}