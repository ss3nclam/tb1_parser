TB1: dict = {
    'Ai': {
        'regex': {
            'sheet': {
                'validate': {
                    'name': r'^.*([Вв]х|[Аа]налог).*([Вв]х|[Аа]налог).*$'
                }
            },
            'columns': {
                'validate': {
                    'names': {
                        'signal_variable': r'((([Нн]ом([ер]{2}|\.)?)|№)?\s?([Пп]ерем\.?([а-я]+[йян])?))',
                        'signal_name': r'((([Нн]а)?([Ии]м\.?(я|ен\.?(\w+)?))\s?)?([Пп]арам(\.|етр(\.|а)?)))',
                        'signal_range': r'(([Дд]иап\.?(аз\.?)?(он)?\s)([Ии]зм\.?(ер\.?)?(ен\.?)?(ия)?)?)',
                        'signal_warning_range': r'(ПС)',
                        'signal_alarm_range': r'(АС)',
                    }
                },
                'replace': {
                    'trash': {
                        'pattern': r'(\(.*?\))|\n|\-',
                        'new_value': ''
                    }
                }
            },
            'content': {
                'validate': {
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
            }
        },
        # Необходимо соблюдать порядок столбцов, как в ТБ1
        # 'columns': {
        #         'variable': 'A',
        #         'name': 'B',
        #         'range': 'E',
        #         'warning_range': 'F',
        #         'alarm_range': 'G',
        # }
    },
    'Di': {
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
    'Do': {
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
            'sheet_name': 'Аналог. вх',
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