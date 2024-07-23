from pybit.unified_trading import WebSocket, HTTP


class ByBitMethods:
    
    def __init__(self, api_key=None, api_secret=None, interval=5, symbol='BTCUSDT', category='linear'):
        self.api_key = api_key
        self.api_secret = api_secret
        self.interval = interval
        self.symbol = symbol
        self.category = category


    # WebSocket method

    def ws_stream(self, callback):
        ws = WebSocket(
            testnet=False,
            channel_type=self.category,
        )

        ws.kline_stream(
            symbol=self.symbol,
            interval=self.interval,
            callback=callback
        )


    # HTTP method   

    def http_query(self):
        session = HTTP()
        http_response = session.get_kline(category=self.category, symbol=self.symbol, interval=self.interval,)

        # print(http_response)

        return http_response['result']['list']