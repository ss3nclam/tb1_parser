class AiSignal(object):

    def __init__(self) -> None:
        self.variable: None | str
        self.name: None | str
        self.LL: None | str
        self.LA: None | str
        self.LW: None | str
        self.HW: None | str
        self.HA: None | str
        self.HL: None | str


    def __repr__(self) -> str:
        return f'Var: {self.variable}\nName: {self.name}\nLL: {self.LL}\nHL: {self.HL}\nLA: {self.LA}\nHA: {self.HA}\nLW: {self.LW}\nHW: {self.HW}\n'