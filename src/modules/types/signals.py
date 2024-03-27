from dataclasses import dataclass


@dataclass
class Signal(object):
    
    def __init__(self) -> None:
        self.variable: None | str
        self.name: None | str
        self.formated_name: None | str
        self.plc_module: None | str


    def __repr__(self) -> str:
        return f'Var: {self.variable},\nName: {self.name},\nFormated_name: {self.formated_name},\nPLC_module: {self.plc_module}'


@dataclass
class AiSignal(Signal):

    def __init__(self) -> None:
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
        return super().__repr__() + f',\nUnit: {self.unit},\nLL: {self.LL},\nLA: {self.LA},\nLW: {self.LW},\nHW: {self.HW},\nHA: {self.HA},\nHL: {self.HL},\nLE: {self.LE},\nHE: {self.HE}\n'