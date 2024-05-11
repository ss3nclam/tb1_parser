from dataclasses import dataclass

from .plc_module import PLCModule


@dataclass
class Signal(object):
    
    def __init__(self) -> None:
        '''
        Дата-класс. Шаблон для наследования.
        '''
        self.variable: None | str
        self.name: None | str
        # self.formated_name: None | str
        self.plc_module: None | PLCModule
        self.plc_channel: None | int


    def __repr__(self) -> str:
        params: str = '(' + ', '.join(f'{key}: {value}' for key, value in self.__dict__.items()) + ')'
        return self.__class__.__name__ + params
    

    def isused(self) -> bool:
        return self.name.lower() != 'резерв'


    def isprotected(self) -> bool:
        pass  # FIXME Заглушка метода для родителя
