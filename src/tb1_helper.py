from re import fullmatch


types_regex = {
    'Ai': r'^.*([Вв]х|[Аа]налог).*([Вв]х|[Аа]налог).*$',
    'Di': r'^.*([Вв]х|[Дд]искр).*([Вв]х|[Дд]искр).*$',
    'Do': r'^.*([Вв]ых|[Дд]искр).*([Вв]ых|[Дд]искр).*$'
}


class TB1Helper:

    @staticmethod
    def search_sheet(names_list: list, content_type: str) -> str | None:
        'Return name of the sheet by content type'
        #TODO Валидатор
        #TODO Логи

        reg = types_regex.get(content_type)

        for name in names_list:
            match = fullmatch(reg, name)
            if match:
                return match.string
        return None