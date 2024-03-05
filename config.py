TB1 = {
    'Ai_SHEET': {
        'regex': r'^.*([Вв]х|[Аа]налог).*([Вв]х|[Аа]налог).*$',
        'columns': {
            'variable': 'A',
            'name': 'B',
            'range': 'E',
            'alarm_range': 'G',
            'warning_range': 'H',
            'error_range': 'I'
        }
    },
    'Di_SHEET': {
        'regex': r'^.*([Вв]х|[Дд]искр).*([Вв]х|[Дд]искр).*$',
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
        'regex': r'^.*([Вв]ых|[Дд]искр).*([Вв]ых|[Дд]искр).*$',
        'columns': {
            'variable': 'A',
            'name': 'B',
            'logic_value': 'F'
            # TODO Дописать все нуженые поля
        }
    }
}

PARSER = {
    'for_ranges': {}
}