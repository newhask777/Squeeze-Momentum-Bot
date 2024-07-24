from bybit import ByBitMethods
from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json
import time

def get_klines(message):
    print(message)


def main():
    ws = 'websocket'
    # http = 'http'
    ind = Indicators(ws, symbol='TONUSDT', save_ws=True, save_http=True)
    ind.sma_20()


if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)
        


