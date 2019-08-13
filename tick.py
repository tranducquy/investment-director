

def get_tick(symbol):
    if symbol.endswith('=X') == 1 or symbol.startswith('^') == 1: #為替と株式指数
        tick = 0.01
    elif symbol.find('-') >= 1: #暗号通貨
        tick = 0.0001
    elif symbol.endswith('.T') == 1: #日本株
        tick = 1
    else: #未知
        tick = 0.01
    return tick