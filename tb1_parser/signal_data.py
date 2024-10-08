from dataclasses import dataclass

from transliterate import translit

from .plc_module import PLCModule


@dataclass
class SignalData(object):
    
    def __init__(self) -> None:
        '''
        Дата-класс. Шаблон для наследования.
        '''
        self.variable: None | str = None
        self.name: None | str = None
        self.formated_name: None | str = None
        self.plc_module: None | PLCModule = None
        self.plc_channel: None | int = None

    def isused(self) -> bool:
        return translit(self.name, 'ru', reversed=True).lower() not in ('rezerv', 'net podkljuchenija', 'ne podkljucheno')

    def isprotected(self) -> bool:
        pass  # FIXME Заглушка метода для родителя

    def set_formated_name(self, inp_name: str):
        self.formated_name = inp_name

    def __repr__(self) -> str:
        params: str = '(' + '; '.join(f'{key}: {value}' for key, value in self.__dict__.items()) + ')'
        return self.__class__.__name__ + params
