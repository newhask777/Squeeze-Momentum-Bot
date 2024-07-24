from pybit.unified_trading import WebSocket, HTTP
from pybit import exceptions
import time

from db.conn import engine, SessionLocal, Base
from db.models import WsCandle, HttpCandle


class ByBitMethods:
    
    def __init__(self, api_key=None, api_secret=None, interval=5, symbol='BTCUSDT', category='linear', save_ws=False, save_http=True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.interval = interval
        self.symbol = symbol
        self.category = category
        self.stream_type = ''
        self.save_ws = save_ws
        self.save_http = save_http

        Base.metadata.create_all(bind=engine)
        # db = SessionLocal()

    # WebSocket method

    def ws_stream(self):
        self.stream_type = 'websocket'

        def get_klines(message):
            print(message)

        try:
            ws = WebSocket(
                testnet=False,
                channel_type=self.category,
            )

            ws.kline_stream(
                symbol=self.symbol,
                interval=self.interval,
                callback=get_klines
            )

            if self.save_ws:
                print('save ws')
                
            if self.save_http:
                print('save http')

        except exceptions.InvalidRequestError as e:
            print("Bybit Request Error", e.status_code, e.message, sep=' | ')
        except exceptions.FailedRequestError as e:
                print("Bybit Request Failed", e.status_code, e.message, sep=' | ')
        except Exception as e:
            print(e)



    # HTTP method   

    def http_query(self):
        self.stream_type = 'http'

        session = HTTP()
        http_response = session.get_kline(category=self.category, symbol=self.symbol, interval=self.interval,)

        # print(http_response)

        return self.stream_type, http_response['result']['list']