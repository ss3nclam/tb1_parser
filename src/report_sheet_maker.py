import logging

import pandas

import config
from src.ai_signal import AiSignal
from src.ai_storage import AiStorage
from src.di_storage import DiStorage
from src.do_storage import DoStorage
from src.report_sheet import ReportSheet


class ReportSheetMaker:

    def __init__(self) -> None:
        pass


    def get_empty(self, signals: AiStorage | DiStorage | DoStorage) -> ReportSheet | None:
        try:
            if isinstance(signals, AiStorage):
                signals: AiStorage
                sheet = pandas.DataFrame({column: [] for column in config.REPORT['sheets']['Ai']['columns']})
                if len(list(sheet)) < 3:
                    raise ValueError
                for signal in signals:
                    signal: AiSignal
                    sheet.loc[len(sheet.index)] = [signal.name, 'знач.', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.LL:
                        sheet.loc[len(sheet.index)] = ['NaN', 'НГ', signal.LL, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.LA:
                        sheet.loc[len(sheet.index)] = ['NaN', 'НА', signal.LA, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.LW:
                        sheet.loc[len(sheet.index)] = ['NaN', 'НП', signal.LW, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.HW:
                        sheet.loc[len(sheet.index)] = ['NaN', 'ВП', signal.HW, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.HA:
                        sheet.loc[len(sheet.index)] = ['NaN', 'ВА', signal.HA, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']
                    if signal.HL:
                        sheet.loc[len(sheet.index)] = ['NaN', 'ВГ', signal.HL, 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN']

                

            elif isinstance(signals, DiStorage):
                pass

            elif isinstance(signals, DoStorage):
                pass

            else:
                raise TypeError(f'{type(signals)} не является допустимым типом передаваемого объекта')

        except Exception as error:
            logging.error(f'ReportSheetMaker: ошибка создания листа - {error}')
            sheet = None

        finally:
            return sheet