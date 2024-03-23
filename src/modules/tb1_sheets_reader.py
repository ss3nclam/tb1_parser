import logging
import re
from typing import Literal

from pandas import ExcelFile
from config import TB1 as config


class TB1SheetsReader:

    def __init__(self, file: ExcelFile) -> None:
        self.__logs_owner: str = self.__class__.__name__

        self.__file = file
    

    def __find_sheet_name(self, searched_content: Literal['Ai', 'Di', 'Do']) -> str | None:
        logging.info(f'{self.__logs_owner}: поиск листа "{searched_content}"..')
        matches: list[str] = []
        try:
            for sheet_name in map(str, self.__file.sheet_names):
                name_pattern = config[f'{searched_content}']['regex']['sheet']['validate']['name']
                if match := re.fullmatch(name_pattern, sheet_name):
                    matches.append(match.string)

            matches_count: int = len(matches)
            if matches_count == 1:
                out: str = matches[0]
                logging.info(f'{self.__logs_owner}: лист "{searched_content}" успешно найден - "{out}"')
                return out
            else:
                raise ValueError(f'некорректное число совпадений с шаблоном ({matches_count})')
            
        except Exception as error:
            error = 'в файле конфигурации не найден шаблон для поиска' if type(error) is KeyError else error
            logging.error(f'{self.__logs_owner}: ошибка поиска листа "{searched_content}" - {error}')
            return


    def test(self):
        for i in ('Ai', 'Di', 'Do'):
            self.__find_sheet_name(i)