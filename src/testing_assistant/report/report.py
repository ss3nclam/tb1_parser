import logging
from testing_assistant.report.sheets import ReportAiSheet, ReportDiSheet, ReportDoSheet


class Report(object):

    def __init__(self) -> None:
        self.__sheets: dict

    
    def add_sheet(self, sheet: ReportAiSheet | ReportDiSheet | ReportDoSheet):
        self.__sheets['Ai'] = sheet

