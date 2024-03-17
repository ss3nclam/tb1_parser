from pandas import ExcelFile
from src.tb1.sheets import TB1AiSheet, TB1DiSheet, TB1DoSheet


class TB1(object):

    def __init__(self, filepath: str) -> None:
        self.__file = ExcelFile(filepath)
        self.__sheet_names = self.__file.sheet_names

        self.Ai_sheet: TB1AiSheet | None = None
        self.Di_sheet: TB1DiSheet | None = None
        self.Do_sheet: TB1DoSheet | None = None
    

    def read(self) -> bool:
        try:
            pass
        except Exception:
            pass

    
    def test(self):
        return self.__sheet_names