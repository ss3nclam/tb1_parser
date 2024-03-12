from pandas import DataFrame

from testing_assistant.config import REPORT as config


config = config['sheets']


class ReportAiSheet(DataFrame):
    SHEET_TYPE = 'Ai'
    SHEET_NAME = config[SHEET_TYPE]['sheet_name']

    @property
    def _constructor(self):
        return ReportAiSheet


class ReportDiSheet(DataFrame):
    SHEET_TYPE = 'Ai'
    SHEET_NAME = config[SHEET_TYPE]['sheet_name']

    @property
    def _constructor(self):
        return ReportDiSheet
    

class ReportDoSheet(DataFrame):
    SHEET_TYPE = 'Ai'
    SHEET_NAME = config[SHEET_TYPE]['sheet_name']

    @property
    def _constructor(self):
        return ReportDoSheet