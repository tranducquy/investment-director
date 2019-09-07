# -*- coding: utf-8 -*-

def get_tick(symbol):
    if symbol == 'GBP=X': #USD/GBP
        tick = 0.0001
    elif symbol.endswith('=X') == 1 or symbol.startswith('^') == 1: #為替と株式指数
        tick = 0.01
    elif symbol.endswith('.T') == 1: #日本株
        tick = 1
    elif 'XBTUSD' in symbol: #bitmex xbtusd
        tick = 0.5
    elif 'ETHUSD' in symbol: #bitmex ethusd
        tick = 0.05
    else: #未知
        tick = 0.01
    return tick
