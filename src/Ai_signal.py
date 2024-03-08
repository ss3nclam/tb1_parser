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
        return f'Name: {self.name}\nLL: {self.LL}\nLA: {self.LA}\nLW: {self.LW}\nHW: {self.HW}\nHA: {self.HA}\nHL: {self.HL}\n'
