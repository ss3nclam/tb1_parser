class Signal(object):
    
    def __init__(self) -> None:
        self.variable = None
        self.name = None
        self.plc_module = None


    def __repr__(self) -> str:
        return f'Var: {self.variable}, Name: {self.name}, PLC_module: {self.plc_module}'


class AiSignal(Signal):

    def __init__(self) -> None:
        super().__init__()
        self.unit = None
        self.LL = None
        self.LA = None
        self.LW = None
        self.HW = None
        self.HA = None
        self.HL = None
    

    def __repr__(self) -> str:
        return super().__repr__() + f', Unit: {self.unit}, LL: {self.LL}, LA: {self.LA}, LW: {self.LW}, HW: {self.HW}, HA: {self.HA}, HL: {self.HL}'