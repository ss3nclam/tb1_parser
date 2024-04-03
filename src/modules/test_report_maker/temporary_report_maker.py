import logging

import numpy
from pandas import DataFrame, ExcelWriter

from src.modules.tb1_parser.types.di_signal import DiSignal
from src.modules.tb1_parser.types.do_signal import DoSignal
from src.modules.tb1_parser.types.ai_signal import AiSignal
from src.modules.tb1_parser.types.signals_collection import \
    SignalsCollection
from src.modules.tb1_parser.types.parsed_tb1_collection import \
    ParsedTB1Collection


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


class TemporaryReportMaker:

    def __init__(self, parsed_tb1: ParsedTB1Collection) -> None:
        self.__logs_owner = self.__class__.__name__
        self.__tb1 = parsed_tb1

        self.__report: dict = {}


    # REFACT Полностью переписать метод создания листа на xlsxwriter
    def __make_signal_sheet(self, collection: SignalsCollection) -> DataFrame:
        try:
            if isinstance(collection, SignalsCollection):
                columns = REPORT_CONFIG['Ai']['columns']
                sheet = DataFrame(columns=columns)
                for signal in (signal for signal in collection if signal.name.lower() != 'резерв'):
                    signal: AiSignal
                    sheet.loc[len(sheet.index)] = [signal.name, 'знач.', *['']*(len(columns) - 2)]
                    setpoints = {'НГ': signal.LL, 'НА': signal.LA, 'НП': signal.LW, 'ВП': signal.HW, 'ВА': signal.HA, 'ВГ': signal.HL}
                    for name, value in setpoints.items():
                        value: float | None
                        if value is not None:
                            sheet.loc[len(sheet.index)] = [numpy.nan, name, round(value) if value.is_integer() else value, *['']*(len(columns) - 3)]
            if isinstance(collection, SignalsCollection):
                columns = REPORT_CONFIG['Di']['columns']
                sheet = DataFrame(columns=columns)
                for signal in (signal for signal in collection if signal.name.lower() != 'резерв'):
                    signal: DiSignal
                    logic_value = signal.logic_value
                    sheet.loc[len(sheet.index)] = [signal.name, (logic_value if logic_value is not None else 'X'), *['']*(len(columns) - 2)]
            if isinstance(collection, SignalsCollection):
                columns = REPORT_CONFIG['Do']['columns']
                sheet = DataFrame(columns=columns)
                for signal in (signal for signal in collection if signal.name.lower() != 'резерв'):
                    signal: DoSignal
                    logic_value = signal.logic_value
                    sheet.loc[len(sheet.index)] = [signal.name, (logic_value if logic_value is not None else 'X'), *['']*(len(columns) - 2)]
        finally:
            return sheet


    def make(self):
        try:
            logging.info(f'{self.__logs_owner}: начало формирования отчёта..')
            for sheet_type, collection in self.__tb1.items():
                match sheet_type:
                    case 'Ai':
                        output_df = self.__make_signal_sheet(collection)
                    case 'Di':
                        output_df = self.__make_signal_sheet(collection)
                    case 'Do':
                        output_df = self.__make_signal_sheet(collection)
                    case _:
                        raise ValueError('передан неопознанный тип листа')
                self.__report[sheet_type] = output_df
                logging.info(f'{self.__logs_owner}:{sheet_type}: лист успешно сформирован')
        except Exception as error:
            logging.error(f'{self.__logs_owner}: ошибка создания отчёта - {error}')


    # REFACT Переписать метод записи в файл
    def write(self, filepath: str):
        try:
            writer = ExcelWriter(filepath, engine='xlsxwriter')
            for sheet_type, sheet in self.__report.items():
                sheet_name = REPORT_CONFIG[sheet_type]['sheet_name']
                sheet: DataFrame
                sheet.to_excel(writer, sheet_name=sheet_name, index=False)
            writer.close()
        except Exception as exception:
            print(exception)
        finally:
            pass