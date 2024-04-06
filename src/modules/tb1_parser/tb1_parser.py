import logging

from src.modules.tb1_parser._regex_lib import TB1 as config
from src.modules.tb1_parser._ai_sheet_parser import AiSheetParser
from src.modules.tb1_parser._di_sheet_parser import DiSheetParser
from src.modules.tb1_parser._do_sheet_parser import DoSheetParser
from src.modules.tb1_parser.types.parsed_tb1_collection import \
    ParsedTB1Collection
from src.modules.tb1_parser.types.tb1_readed_sheets_collection import \
    TB1ReadedSheetsCollection
from src.modules.tb1_parser._tb1_file_reader import TB1FileReader


all_avaible_sheets = list(config)


class TB1Parser:

    def __init__(self, filepath: str) -> None:
        self.__logs_owner: str = self.__class__.__name__
        self.__readed_sheets: TB1ReadedSheetsCollection = self.__get_readed_sheets(filepath)

        self.collection: ParsedTB1Collection = {}
    

    def __get_readed_sheets(self, filepath: str) -> TB1ReadedSheetsCollection:
        file_reader = TB1FileReader(filepath)
        file_reader.read()
        out = file_reader.sheets

        return out


    def read(self):
        try:
            for sheet_type, sheet_dataframe in self.__readed_sheets.items():
                logging.info(f'{self.__logs_owner}:{sheet_type}: начало парсинга..')
                match sheet_type:
                    case 'Ai':
                        parser = AiSheetParser(sheet_dataframe)
                    case 'Di':
                        parser = DiSheetParser(sheet_dataframe)
                    case 'Do':
                        parser = DoSheetParser(sheet_dataframe)
                    case _:
                        raise ValueError('передан неопознанный тип листа')
                parser.start()
                self.collection[sheet_type] = parser.get_result()
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка парсинга входных листов - {error}')
    

    # def get(self, collection: Literal['Ai', 'Di', 'Do']) -> TB1ParsedSheetsCollection:
    #     if out := self.sheets_collections:
    #         return out.get()
    #     else:
    #         logging.error(f'{self.__logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
    #         raise IndentationError