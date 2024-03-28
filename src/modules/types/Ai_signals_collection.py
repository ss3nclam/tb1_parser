class AiSignalsCollection(tuple):
    
    def get_formated_names(self):
        return tuple(i.formated_name for i in self)