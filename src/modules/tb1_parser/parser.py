import logging

from src.modules.tb1_parser.ai_sheet_parser import AiSheetParser
from src.modules.types.signals_collection import SignalsCollection
from src.modules.types.tb1_readed_sheets import TB1ReadedSheets


class TB1Parser:

    def __init__(self, readed_sheets_obj: TB1ReadedSheets) -> None:
        self.__logs_owner: str = self.__class__.__name__

        self.__sheets_dict = readed_sheets_obj
        self.__result: SignalsCollection = {}
    

    def start(self):
        try:
            for sheet_type, sheet_dataframe in self.__sheets_dict.items():
                match sheet_type:
                    case 'Ai':
                        parser = AiSheetParser(sheet_dataframe)
                    case 'Di':
                        continue # TODO Написать парсера Di листов
                    case 'Do':
                        continue # TODO Написать парсера Do листов
                parser.start()
                self.__result[sheet_type] = parser.get_result()
        except Exception as error:
            pass # TODO Написать обработку исключений
    

    def get_result(self) -> SignalsCollection:
        if out := self.__result:
            return out
        else:
            logging.error(f'{self.__logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
            raise IndentationError