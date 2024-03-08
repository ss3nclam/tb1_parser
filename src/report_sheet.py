from typing import Literal
from pandas import DataFrame


class ReportSheet(DataFrame):

    def __init__(self, sheet_type: Literal['Ai', 'Di', 'Do']) -> None:
        super().__init__()
        self.sheet_type = sheet_type
