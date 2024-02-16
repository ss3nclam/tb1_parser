from pandas import DataFrame


class TB1Sheet:

    def __init__(self, data_frame) -> None:
        self.sheet: DataFrame = data_frame


    def test(self) -> DataFrame:
        return self.sheet