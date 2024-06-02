import logging
from types import FunctionType

from .signals_collection import SignalsCollection


class ParsedTB1Collection(dict):

    @property
    def __logs_owner(self) -> str:
        return self.__class__.__name__

    def filter(self, key: FunctionType):
        """Фильтрация сигналов в коллекции"""
        filtered = ParsedTB1Collection()
        try:
            if not isinstance(key, FunctionType):
                raise TypeError("передан некорректный тип атрибута 'key'")
            
            for type, collection in self.items():
                filtered[type] = SignalsCollection(
                    signal for signal in collection if key(signal)
                )
            return filtered
        
        except Exception as error:
            logging.error(f"{self.__logs_owner}: ошибка фильтрации сигналов: {error}")
