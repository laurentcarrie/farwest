
def check_type(o, t):
    if isinstance(o, t):
        return
    raise TypeError(f'o is of type{type(o)}, but expected {t}')
