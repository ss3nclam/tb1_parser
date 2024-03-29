import logging

from src.modules.regex_lib import TB1 as config
from src.modules.tb1_parser.ai_sheet_parser import AiSheetParser
from src.modules.tb1_parser.di_sheet_parser import DiSheetParser
from src.modules.tb1_parser.do_sheet_parser import DoSheetParser
from src.modules.tb1_parser.types.parsed_tb1_collection import \
    ParsedTB1Collection
from src.modules.tb1_reader.types.tb1_readed_sheets_collection import \
    TB1ReadedSheetsCollection


all_avaible_sheets = list(config)


class TB1Parser:

    def __init__(self, readed_sheets: TB1ReadedSheetsCollection) -> None:
        self.__logs_owner: str = self.__class__.__name__
        self.__readed_sheets = readed_sheets

        self.collection: ParsedTB1Collection = {}
    

    def start(self):
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