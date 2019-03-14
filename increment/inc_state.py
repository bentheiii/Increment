# change = (after/before)-1
# after = (change + 1)*before
# before = after/(change + 1)

from increment.__util__ import parse_float


# the calc functions return a tuple of text to display and an optional stylesheet to apply

def num_format(n):
    return format(n, ',.2f'), None


def calc_before(before, after, change):
    after = parse_float(after)
    change = parse_float(change)

    ret = after / (change + 1)
    return num_format(ret)


def calc_after(before, after, change):
    before = parse_float(before)
    change = parse_float(change)

    ret = (change + 1) * before
    return num_format(ret)


def change_format(n):
    ret = format(n*100, '+,.2f')
    stylesheet = ''
    if n < 0:
        stylesheet = 'color: red;'
    elif n > 0:
        stylesheet = 'color: darkgreen;'

    return ret, stylesheet


def calc_change(before, after, change):
    before = parse_float(before)
    after = parse_float(after)

    ret = (after / before) - 1
    return change_format(ret)
