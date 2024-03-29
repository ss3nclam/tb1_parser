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
        return f'var: {self.variable}, formated_name: {self.formated_name}, module: {self.plc_module}'