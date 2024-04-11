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
                        'variable': r'^.*((([Нн]ом([ер]{2}|\.)?)|№)?\s?([Пп]ерем\.?([а-я]+[йян])?)).*$',
                        'name': r'^.*((([Нн]а)?([Ии]м\.?(я|ен\.?(\w+)?))\s?)([Пп]арам(\.|етр(\.|а))|сигнала)).*$',
                        'unit': r'^.*([Ее]диница измерения).*$',
                        'range': r'^.*(([Дд]иап\.?(аз\.?)?(он)?\s)([Ии]зм\.?(ер\.?)?(ен\.?)?(ия)?)?).*$',
                        'warning_range': r'^.*(ПС).*$',
                        'alarm_range': r'^.*(АС).*$',
                        'error_range': r'^.*(НС).*$',
                        'plc_module': r'^.*([Мм]одуль\s(\w+)?).*$',
                        'plc_channel': r'^.*([Кк]анал).*$'
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
                    'simple_range': r'^(([0-9]+[.,])?[0-9]+)\s?\-\s?(([0-9]+[.,])?[0-9]+)(\s?\D+)?$',
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
        }
    },
    'Di': {
        'regex': {
            'sheet': {
                'validate': {
                    'name': r'^.*([Вв]х|[Дд]искр).*([Вв]х|[Дд]искр).*$'
                }
            },
            'columns': {
                'validate': {
                    'names': {
                        'variable': r'^.*((([Нн]ом([ер]{2}|\.)?)|№)?\s?([Пп]ерем\.?([а-я]+[йян])?)).*$',
                        'name': r'^.*((([Нн]а)?([Ии]м\.?(я|ен\.?(\w+)?))\s?)([Пп]арам(\.|етр(\.|а))|сигнала)).*$',
                        'logic_value': r'^.*[Лл]ог(\w+)?\.?\s?[Зз]нач(\w+)?\.?',
                        'alarm_signal': r'^.*(АС).*$',
                        'warning_signal': r'^.*(ПС).*$',
                        'tele_signal': r'^.*(ТС).*$',
                        'error_signal': r'^.*(НС).*$',
                        'plc_module': r'^.*([Мм]одуль\s(\w+)?).*$',
                        'plc_channel': r'^.*([Кк]анал).*$'
                    }
                },
                'replace': {
                    'trash': {
                        'pattern': r'(\(.*?\))|\n|\-',
                        'new_value': ''
                    }
                }
            },
        },
    },
    'Do': {
        'regex': {
            'sheet': {
                'validate': {
                    'name': r'^.*([Вв]ых|[Дд]искр).*([Вв]ых|[Дд]искр).*$'
                }
            },
            'columns': {
                'validate': {
                    'names': {
                        'variable': r'^.*((([Нн]ом([ер]{2}|\.)?)|№)?\s?([Пп]ерем\.?([а-я]+[йян])?)).*$',
                        'name': r'^.*((([Нн]а)?([Ии]м\.?(я|ен\.?(\w+)?))\s?)([Пп]арам(\.|етр(\.|а))|сигнала)).*$',
                        'logic_value': r'^.*[Лл]ог(\w+)?\.?\s?[Зз]нач(\w+)?\.?',
                        'plc_module': r'^.*([Мм]одуль\s(\w+)?).*$',
                        'plc_channel': r'^.*([Кк]анал).*$'
                    }
                },
                'replace': {
                    'trash': {
                        'pattern': r'(\(.*?\))|\n|\-',
                        'new_value': ''
                    }
                }
            }
        }
    }
}

PARSER = {
    'signals': {
        'format_variable_name': {
            r'\((\w+\b\s?){4,}\)': '',
            r'[\.\(\)\=\%\>\<\\\|\/\№\≤\≥\"\'\«\»]': '',
            r'[Тт]очк\w+\b\s': 'т',
            r'[Гг]рупп\w+\b\s': 'г',
            r'[Оо]порн\w+\b\s[Пп]одш\w+\b': 'ОП',
            r'[Оо]порн\w+\b\-[Уу]порн\w+\b\s[Пп]одш\w+\b': 'ОУП',
            r'[Пп]одш\w+\b': 'подш',
            r'([Пп]о\s)?[Оо]с[иь]\s?': '',
            r'[Вв]ибр((\w+\b)|\.)?': 'Вибр',
            r'[Вв]озб((\w+\b)|\.)?': 'Возб',
            r'[Вв]кл((\w+\b)|\.)?': 'Вкл',
            r'[Оо]ткл((\w+\b)|\.)?': 'Откл',
            r'[Оо]ткр((\w+\b)|\.)?': 'Откр',
            r'[Зз]акр((\w+\b)|\.)?': 'Закр',
            'Температура': 'T',
            'Давление': 'P',
            'Перепад давления': 'dP',
            'Ток': 'I',
            'Напряжение': 'U',
            'Уровень': 'L'
        },
        # 'find_plc_module': r'^\w{2}\-[a-z0-9-]+\,?\s+?\(?(\w(\d+).?(\d+))\)?$'
        'find_plc_module': r'([IOAD]+.?\d+\D\d+)\s{0,}\(?(\D?\d+\-\d+)\)?'
    }
}