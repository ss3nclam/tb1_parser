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
        self.plc_channel: None | int


    def __repr__(self) -> str:
        params: str = '(' + ', '.join(f'{param_name}: {param_value}' for param_name, param_value in self.__dict__.items()) + ')'
        return self.__class__.__name__ + params
    

    def isreserv(self) -> bool:
        return self.name.lower() == 'резерв'