from typing import Literal

from src.modules.tb1_parser.types._signal import Signal


class DoSignal(Signal):

    def __init__(self) -> None:
        '''
        Дата-класс для дискретных выходных сигналов, потомок 'Signal'.
        '''
        super().__init__()
        self.logic_value: None | Literal[1, 0]

    
    def __repr__(self) -> str:
        out: str = \
            f', logic_value: {self.logic_value}'
        return super().__repr__() + out
            