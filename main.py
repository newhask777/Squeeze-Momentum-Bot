from bybit import ByBitMethods
from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json
import time

from db.conn import engine, SessionLocal, Base
from db.models import WsCandle, HttpCandle

Base.metadata.create_all(bind=engine)
db = SessionLocal()


def main():
    ws = 'websocket'
    _http = 'http'
    ind = Indicators(_http, symbol='TONUSDT', save_ws=False, save_http=True, db=db)
    ind.sma_20()

    while True:
        main()
        time.sleep(5)


if __name__ == '__main__':
    main()
        
        


