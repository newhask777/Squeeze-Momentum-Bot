from pybit.unified_trading import WebSocket
from pybit import exceptions
import pandas as pd
import time

from datetime import datetime
from db.models import WsCandle
from db.conn import engine, SessionLocal, Base

Base.metadata.create_all(bind=engine)
db = SessionLocal()

def save_to_db(message):
   
    print(message)
    print('info')

    try:
        for m in message['data']:
            kline_info = WsCandle()
            unix_timestamp = m['timestamp']       
            stamp = datetime.fromtimestamp(unix_timestamp / 1000)
            stamp = stamp.strftime("%Y-%m-%d %H:%M:%S")
            # print(stamp)
            kline_info.stamp =  stamp
            kline_info.open = m['open']
            kline_info.high = m['high']
            kline_info.low = m['low']
            kline_info.close = m['close']
            kline_info.volume = m['volume']

            db.add(kline_info)
            db.commit()
    except:
        print('DB ERROR')

    # time.sleep(20)

 

def start_stream():   
    # time.sleep(20)
    try:
        ws = WebSocket(
            testnet=False,
            channel_type='linear',
        )

        ws.kline_stream(
            symbol="TONUSDT",
            interval=5,
            callback=save_to_db
        )  
        print('saved')

    except exceptions.InvalidRequestError as e:
            print("Bybit Request Error", e.status_code, e.message, sep=' | ')
    except exceptions.FailedRequestError as e:
                print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
    except Exception as e:
            print(e)
      

while True:
      start_stream()
      time.sleep(10)

           