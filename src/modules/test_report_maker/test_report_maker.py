from dataclasses import dataclass

from pandas import DataFrame

from src.modules.tb1_parser.types.parsed_tb1_collection import \
    ParsedTB1Collection
from src.modules.test_report_maker.types.test_report import TestReport


class TestReportMaker:

    def __init__(self, parsed_collection: ParsedTB1Collection) -> None:
        self.__logs_owner = self.__class__.__name__

        self.__parsed_collection = parsed_collection
        self.__report = TestReport()


    def __make_Ai_sheet(self):
        try:
            Ai_signals = self.__parsed_collection['Ai']
        except Exception as error:
            pass
        finally:
            pass

    
    def __make_Di_sheet(self):
        pass
    
    
    def __make_Do_sheet(self):
        pass
    
    
    def __make_logics_sheet(self):
        pass
    
    
    def __make_protections_sheet(self):
        pass
 
 
    def __make_diagnostics_sheet(self):
        pass


    def init_sheets(self):
        pass


    def write_to_excel(self, filepath: str):
        pass
