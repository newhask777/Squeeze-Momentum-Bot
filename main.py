from indicators import Indicators
from pybit.unified_trading import WebSocket, HTTP
import json
import time

from db.conn import engine, SessionLocal, Base


Base.metadata.create_all(bind=engine)
db = SessionLocal()

ws = 'websocket'
_http = 'http'
ind = Indicators(_http, symbol='TONUSDT', save_ws=True, save_http=False, db=db)

def main():
 
    ind.sma_20()

    # while True:
    #     time.sleep(5)


if __name__ == '__main__':
    while True:
        time.sleep(5)
        main()
        
        


