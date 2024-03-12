from pandas import DataFrame


class TB1AiSheet(DataFrame):
    @property
    def _constructor(self):
        return TB1AiSheet


class TB1DiSheet(DataFrame):
    @property
    def _constructor(self):
        return TB1DiSheet
    

class TB1DoSheet(DataFrame):
    @property
    def _constructor(self):
        return TB1DoSheet