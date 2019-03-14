from locale import atof, setlocale, LC_NUMERIC

setlocale(LC_NUMERIC, '')


def parse_float(s: str):
    if s.endswith('%'):
        return parse_float(s[:-1]) / 100
    if not s:
        raise ValueError("can't convert empty string to float")
    return atof(s)
