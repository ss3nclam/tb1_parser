from src.modules.types.signal import Signal


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
        return super().__repr__() + f', Unit: {self.unit}, LL: {self.LL}, LA: {self.LA}, LW: {self.LW}, HW: {self.HW}, HA: {self.HA}, HL: {self.HL}, LE: {self.LE}, HE: {self.HE}'
        # return super().__repr__()
        # return super().__repr__() + f',\nUnit: {self.unit},\nLL: {self.LL},\nLA: {self.LA},\nLW: {self.LW},\nHW: {self.HW},\nHA: {self.HA},\nHL: {self.HL},\nLE: {self.LE},\nHE: {self.HE}\n'