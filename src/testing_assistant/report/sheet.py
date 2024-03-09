from typing import Literal
from pandas import DataFrame


class ReportSheet(DataFrame):

    def __init__(self, type: Literal['Ai', 'Di', 'Do'], name: str) -> None:
        super().__init__()
        self.sheet_type = type
        self.sheet_name = name
