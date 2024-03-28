from typing import Literal
from src.modules.tb1_parser.types.signal import Signal


class DiSignal(Signal):

    def __init__(self) -> None:
        super().__init__()
        self.logic_value: None | Literal[1, 0]
        self.alarm_signal: None | bool
        self.warning_signal: None | bool
        self.error_signal: None | bool

    
    def __repr__(self) -> str:
        return super().__repr__() + f', Logic_value: {self.logic_value}, Alarm: {self.alarm_signal}, Warning: {self.warning_signal}, Error: {self.error_signal}'