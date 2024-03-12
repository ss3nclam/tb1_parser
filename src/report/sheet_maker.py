import logging

import config
from src.report.sheets import ReportAiSheet
from src.signals.ai_signal import AiSignal
from src.signals.ai_signal_list import AiSignalList
from src.signals.di_signal_list import DiSignalList
from src.signals.do_signal_list import DoSignalList


class ReportSheetMaker:

    def __init__(self) -> None:
        pass


    def get_empty(self, signals: AiSignalList | DiSignalList | DoSignalList) -> ReportAiSheet | None:
        try:
            if isinstance(signals, AiSignalList):
                signals: AiSignalList
                sheet_config = config.REPORT['sheets']['Ai']
                columns = sheet_config['columns']
                sheet = ReportAiSheet(columns=columns)
                if len(list(sheet)) < 3:
                    raise ValueError
                for signal in signals:
                    signal: AiSignal
                    sheet.loc[len(sheet.index)] = [signal.name, 'знач.', *['']*(len(columns) - 2)]
                    setpoints = {'НГ': signal.LL, 'НА': signal.LA, 'НП': signal.LW, 'ВП': signal.HW, 'ВА': signal.HA, 'ВГ': signal.HL}
                    for name, value in setpoints.items():
                        value: float | None
                        if value is not None:
                            sheet.loc[len(sheet.index)] = ['', name, round(value) if value.is_integer() else value, *['']*(len(columns) - 3)]

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