import logging

from pandas import DataFrame

import config as config
from testing_assistant.signals.ai_signal import AiSignal
from testing_assistant.signals.ai_signal_list import AiSignalList
from testing_assistant.signals.di_signal_list import DiSignalList
from testing_assistant.signals.do_signal_list import DoSignalList
from testing_assistant.report.sheet import ReportSheet


class ReportSheetMaker:

    def __init__(self) -> None:
        pass


    def get_empty(self, signals: AiSignalList | DiSignalList | DoSignalList) -> ReportSheet | None:
        try:
            if isinstance(signals, AiSignalList):
                signals: AiSignalList
                sheet_config = config.REPORT['sheets']['Ai']
                columns = sheet_config['columns']
                sheet = DataFrame({column: [] for column in columns})
                if len(list(sheet)) < 3:
                    raise ValueError
                for signal in signals:
                    signal: AiSignal
                    sheet.loc[len(sheet.index)] = [signal.name, 'знач.', *['NaN']*(len(columns) - 2)]

                    setpoints = {'НГ': signal.LL, 'НА': signal.LA, 'НП': signal.LW, 'ВП': signal.HW, 'ВА': signal.HA, 'ВГ': signal.HL}
                    for name, value in setpoints.items():
                        value: float | None
                        if value is not None:
                            sheet.loc[len(sheet.index)] = ['NaN', name, round(value) if value.is_integer() else value, *['NaN']*(len(columns) - 3)]

            elif isinstance(signals, DiSignalList):
                pass

            elif isinstance(signals, DoSignalList):
                pass

            else:
                raise TypeError(f'{type(signals)} не является допустимым типом передаваемого объекта')

        except Exception as error:
            logging.error(f'ReportSheetMaker: ошибка создания листа - {error}')
            sheet = None

        finally:
            return sheet