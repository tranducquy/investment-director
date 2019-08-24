# -*- coding: utf-8 -*-

def get_tick(symbol):
    if symbol == 'GBP=X': #USD/GBP
        tick = 0.0001
    elif symbol.endswith('=X') == 1 or symbol.startswith('^') == 1: #為替と株式指数
        tick = 0.01
    elif symbol.find('-') >= 1: #暗号通貨
        tick = 0.0001
    elif symbol.endswith('.T') == 1: #日本株
        tick = 1
    elif symbol.find('XBTUSD') >= 1: #bitmex xbtusd
        tick = 1
    elif symbol.find('ETHUSD') >= 1: #bitmex ethusd
        tick = 0.5
    else: #未知
        tick = 0.01
    return tick
