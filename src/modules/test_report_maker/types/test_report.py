from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class TestReport(object):

    def __init__(self):
        self.Ai_sheet: None | DataFrame
        self.Di_sheet: None | DataFrame
        self.Do_sheet: None | DataFrame
        self.logics_sheet: None | DataFrame
        self.protections_sheet: None | DataFrame
        self.diagnostics_sheet: None | DataFrame


    def __repr__(self) -> str:
        return f'{self.__class__.__name__}{tuple(self.__dict__)}'