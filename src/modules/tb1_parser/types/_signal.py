from dataclasses import dataclass


@dataclass
class Signal(object):
    
    def __init__(self) -> None:
        '''
        Дата-класс. Шаблон для наследования.
        '''
        self.variable: None | str
        self.name: None | str
        self.formated_name: None | str
        self.plc_module: None | int | tuple[int]


    def __repr__(self) -> str:
        signal_type: str = self.__class__.__name__
        signal_params: str = str(self.__dict__)[1:-1]
        return f'{signal_type}({signal_params})'