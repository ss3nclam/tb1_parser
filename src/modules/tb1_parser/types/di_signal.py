from src.modules.tb1_parser.types.do_signal import DoSignal


class DiSignal(DoSignal):

    def __init__(self) -> None:
        '''
        Дата-класс для дискретных выходных сигналов, потомок 'Signal -> DoSignal'.
        '''
        super().__init__()
        self.alarm_signal: None | bool
        self.warning_signal: None | bool
        self.error_signal: None | bool

    
    def __repr__(self) -> str:
        out: str = \
            f', alarm: {self.alarm_signal}, ' + \
            f'warning: {self.warning_signal}, ' + \
            f'error: {self.error_signal}'
        return super().__repr__() + out
            