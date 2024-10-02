from .do_signal_data import DoSignalData


class DiSignalData(DoSignalData):

    def __init__(self) -> None:
        '''
        Дата-класс для дискретных выходных сигналов, потомок 'Signal -> DoSignal'.
        '''
        super().__init__()
        self.alarm_signal: None | bool = None
        self.warning_signal: None | bool = None
        self.tele_signal: None | bool = None
        self.error_signal: None | bool = None

    def isprotected(self) -> bool:
        return self.alarm_signal
