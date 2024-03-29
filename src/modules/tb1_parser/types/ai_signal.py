from src.modules.tb1_parser.types._signal import Signal


class AiSignal(Signal):

    def __init__(self) -> None:
        '''
        Дата-класс для аналоговых входных сигналов, потомок '_Signal'.
        '''
        super().__init__()
        self.unit: None | str
        self.LL: None | float
        self.LA: None | float
        self.LW: None | float
        self.HW: None | float
        self.HA: None | float
        self.HL: None | float
        self.LE: None | float
        self.HE: None | float
    

    def __repr__(self) -> str:
        out: str = \
            f', unit: {self.unit}, ' + \
            f'LL: {self.LL}, ' + \
            f'LA: {self.LA}, ' + \
            f'LW: {self.LW}, ' + \
            f'HW: {self.HW}, ' + \
            f'HA: {self.HA}, ' + \
            f'HL: {self.HL}, ' + \
            f'LE: {self.LE}, ' + \
            f'HE: {self.HE}'
        return super().__repr__() + out
