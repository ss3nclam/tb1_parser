from typing import Literal

from .signal_data import SignalData


class DoSignalData(SignalData):

    def __init__(self) -> None:
        '''
        Дата-класс для дискретных выходных сигналов, потомок 'Signal'.
        '''
        super().__init__()
        self.logic_value: None | Literal[1, 0] = None
