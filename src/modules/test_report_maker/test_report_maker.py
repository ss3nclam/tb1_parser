from dataclasses import dataclass

from pandas import DataFrame

from src.modules.tb1_parser.types.parsed_tb1_collection import \
    ParsedTB1Collection
from src.modules.test_report_maker.types.test_report import TestReport


REPORT_CONFIG: dict = {
    'Ai': {
        'sheet_name': 'Аналог. вх.',
        'columns': [
            'Наименование параметра',
            'Тип',
            'Значение уставки',
            'Аналоговые параметры',
            'Главный экран',
            'Всплывающее окно',
            'Сообщения',
            'Тренды',
            'Смена уставок',
            'Вывод в ремонт (графика)',
            'Вывод в ремонт (журнал сообщений)',
            'Вывод в ремонт (блокировка срабатывая защиты)'
        ]
    },
    'Di': {
        'sheet_name': 'Дискр. вх.',
        'columns': [
            "Наименование параметра",
            "Логическое значение",
            "Главный экран",
            "Сообщения",
            "Всплывающее окно",
            "Всплывающее окно",
            "Всплывающее окно",
            "Тип сообщения"
        ]
    },
    'Do': {
        'sheet_name': 'Дискр. вых.',
        'columns': [
            "Наименование параметра",
            "Логическое значение",
            "Индикация команды (для кранов)",
            "Сообщение о подаче команды",
            "Исполнение на имитаторе"
        ]
    }
}


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


    def write_to_excel(self, filename: str):
        pass
