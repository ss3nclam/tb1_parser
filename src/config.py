TB1: dict = {
    'Ai_SHEET': {
        'regex': {
            'validate': {
                'sheet_name': r'^.*([Вв]х|[Аа]налог).*([Вв]х|[Аа]налог).*$',
                'empty_range': r'^\s?[NnAaEeOo]{3,4}|[НнЕеТт]{3}\s?$',
                'range_value': r'([\>\<]?(\-?([0-9]+[.,])?[0-9]+))'
            },
            'replace': {
                'trash': {
                    'pattern': r'(\n|(\+|[Пп]л[а-я]{,2})\.?\s?|([Оо]т|[Дд]о)\s?|\>?\d+\s?[Сс]ек\.?[а-я]{,3}\s?)',
                    'new_value': ''
                    },
                'more': {
                    'pattern': r'([Бб]ол[а-я]{,3}|\>)\s?',
                    'new_value': '>'
                    },
                'less': {
                    'pattern': r'([Мм]ен[а-я]{,3}|\<)\s?',
                    'new_value': '<'
                },
                'minus': {
                    'pattern': r'(\-|([Мм]ин[а-я]{,2}\.?))\s?',
                    'new_value': '-'
                }
            }
        },    
        'columns': {
                'variable': 'A',
                'name': 'B',
                'range': 'E',
                'alarm_range': 'G',
                'warning_range': 'H',
        }
    },
    'Di_SHEET': {
        'regex': {
            'validate': {
                'sheet_name': r'^.*([Вв]х|[Дд]искр).*([Вв]х|[Дд]искр).*$'
            }
        },
        'columns': {
            'variable': 'A',
            'name': 'B',
            'logic_value': 'F',
            'alarm': 'G',
            'warning': 'H',
            'error': 'I',
        }
    },
    'Do_SHEET': {
        'regex': {
            'validate': {
                'sheet_name': r'^.*([Вв]ых|[Дд]искр).*([Вв]ых|[Дд]искр).*$'
            }
        },
        'columns': {
            'variable': 'A',
            'name': 'B',
            'logic_value': 'F'
            # TODO Дописать все нуженые поля
        }
    }
}

REPORT: dict = {
    'sheets': {
        'Ai': {
            'sheet_name': '',
            'columns': [
                'Наименование параметра',
                'Тип',
                'Значение уставки',
                'Аналоговые параметры',
                'Главный экран',
                'Всплывающее окно',
                'Сообщения',
                'Тренды',
                'Смена уставок',
                'Вывод в ремонт (графика)',
                'Вывод в ремонт (журнал сообщений)',
                'Вывод в ремонт (блокировка срабатывая защиты)'
            ]
        },
        'Di': {
            'sheet_name': '',
            'columns': [
                'x'
            ]
        },
        'Do': {
            'sheet_name': '',
            'columns': [
                'x'
            ]
        }
    }
}