from dataclasses import dataclass
import logging

from pandas import DataFrame

from src.modules.tb1_parser.types.ai_signal import AiSignal
from src.modules.tb1_parser.types.di_signal import DiSignal
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


    # REFACT Отрефакторить метод создания Ai листа
    def __make_Ai_sheet(self):
        try:
            columns = REPORT_CONFIG['Ai']['columns']
            sheet = DataFrame(columns=columns)

            for signal in (signal for signal in self.__parsed_collection['Ai'] if signal.name.lower() != 'резерв'):
                signal: AiSignal
                sheet.loc[len(sheet.index)] = [signal.name, 'знач.', *['']*(len(columns) - 2)]
                setpoints = {'НГ': signal.LL, 'НА': signal.LA, 'НП': signal.LW, 'ВП': signal.HW, 'ВА': signal.HA, 'ВГ': signal.HL}
                for name, value in setpoints.items():
                    value: float | None
                    if value is not None:
                        sheet.loc[len(sheet.index)] = ['', name, round(value) if value.is_integer() else value, *['']*(len(columns) - 3)]

            self.__report.Ai_sheet = sheet

        except Exception as error:
            logging.error(f'{self.__logs_owner}:Ai_sheet: ошибка формирования листа - {error}')

    
    # REFACT Отрефакторить метод создания Di листа
    def __make_Di_sheet(self):
        try:
            columns = REPORT_CONFIG['Di']['columns']
            sheet = DataFrame(columns=columns)
            for signal in (signal for signal in self.__parsed_collection['Di'] if signal.name.lower() != 'резерв'):
                signal: DiSignal
                logic_value = signal.logic_value
                sheet.loc[len(sheet.index)] = [signal.name, (logic_value if logic_value is not None else 'X'), *['']*(len(columns) - 2)]

            self.__report.Ai_sheet = sheet

        except Exception as error:
            logging.error(f'{self.__logs_owner}:Di_sheet: ошибка формирования листа - {error}')
    
    
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
