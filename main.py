from bybit import ByBitMethods
from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json

def get_klines(message):
    print(message)


ws = ByBitMethods(symbol='TONUSDT')
ws.ws_stream(get_klines)
# http = ws.http_query()


ind = Indicators(ws)
ind.sma_20()

