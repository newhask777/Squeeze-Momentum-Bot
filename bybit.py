from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
import pandas as pd
import time
import json

from sqlalchemy import event

from datetime import datetime
from db.models import WsCandle, HttpCandle


class ByBitMethods:
    
    def __init__(self, api_key=None, api_secret=None, interval=5, symbol='BTCUSDT', category='linear', save_ws=False, save_http=False, db=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.stream_type = ''
        self.save_ws = save_ws
        self.save_http = save_http
        self.db = db


    # WebSocket method
    def ws_stream(self):
        time.sleep(5)
        self.stream_type = 'websocket'

        def save_to_db(message):
            time.sleep(5)
            print(message)

            try:
                for m in message['data']:
                    kline_info = WsCandle()

                    kline_info.open = m['open']
                    kline_info.high = m['high']
                    kline_info.low = m['low']
                    kline_info.close = m['close']
                    kline_info.volume = m['volume']

                    self.db.add(kline_info)
                    self.db.commit()
            except:
                 print('DB ERROR')


        try:
            ws = WebSocket(
                testnet=False,
                channel_type=self.category,
            )

            ws.kline_stream(
                symbol=self.symbol,
                interval=self.interval,
                callback=save_to_db
            )

           
        except exceptions.InvalidRequestError as e:
            print("Bybit Request Error", e.status_code, e.message, sep=' | ')
        except exceptions.FailedRequestError as e:
                print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
        except Exception as e:
            print(e)



    # HTTP method   
    def http_query(self):
        time.sleep(5)
        self.stream_type = 'http'

        if self.save_http:
                print('save http')

        session = HTTP()
        http_response = session.get_kline(category=self.category, symbol=self.symbol, interval=self.interval,)

        self.db.query(HttpCandle).delete()

        for m in http_response['result']['list']:

            kline_info = HttpCandle()

            unix_timestamp = m[0]
            unix_timestamp = unix_timestamp[:-3]
            unix_timestamp = int(unix_timestamp)

            stamp = datetime.fromtimestamp(unix_timestamp)

            kline_info.stamp = stamp
            kline_info.open = m[1]
            kline_info.high = m[2]
            kline_info.low = m[3]
            kline_info.close = m[4]
            kline_info.volume = m[5]

            self.db.add(kline_info)
            self.db.commit()

            print(http_response)

        # return self.stream_type, http_response['result']['list']