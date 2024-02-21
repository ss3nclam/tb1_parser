from re import fullmatch
from typing import Literal

import config


class TB1Helper:

    @staticmethod
    def search_sheet(names_list: list, content: Literal['Ai', 'Di', 'Do']) -> str | None:
        'Return name of the sheet by content type'
        #TODO Валидатор
        #TODO Логи

        # reg = types_regex.get(content_type)
        reg = config.TB1[f'{content}_SHEET']['regex']

        for name in names_list:
            match = fullmatch(reg, name)
            if match:
                return match.string
        return None