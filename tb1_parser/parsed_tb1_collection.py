from .signals_collection import SignalsCollection


class ParsedTB1Collection(dict):
    
    def filter(self, key):
        """Фильтрация сигналов в коллекции"""
        
        out = ParsedTB1Collection()

        try:
            for signal_type, signal_collection in self.items():
                filtered_collection = (
                    signal for signal in signal_collection if key(signal)
                    )
                out[signal_type] = SignalsCollection(filtered_collection)
            return out
        except Exception as identifier:
            pass
