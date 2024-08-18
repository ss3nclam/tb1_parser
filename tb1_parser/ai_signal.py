from .signal import Signal


class AiSignal(Signal):

    def __init__(self) -> None:
        '''
        Дата-класс для аналоговых входных сигналов, потомок 'Signal'.
        '''
        super().__init__()
        self.unit: None | str = None
        self.LL: None | float = None
        self.LA: None | float = None
        self.LW: None | float = None
        self.HW: None | float = None
        self.HA: None | float = None
        self.HL: None | float = None
        self.LE: None | float = None
        self.HE: None | float = None

    def isprotected(self) -> bool:
        return (self.LA or self.HA) is not None
