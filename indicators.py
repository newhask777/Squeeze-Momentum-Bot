import os
import pandas as pd
import plotly.graph_objects as go
from bybit import ByBitMethods

from db import models
from db.conn import engine, SessionLocal, Base


class Indicators(ByBitMethods):

   
    def __init__(self, bybit_method: str, bybit_methods: dict=None, *args, **kwargs):
        super(Indicators, self).__init__(*args, **kwargs)
        self.bybit_method = bybit_method

        
        if self.bybit_method == 'websocket':
            self.ws_stream()
            

        if self.bybit_method == 'http':
            self.http_query()


        if bybit_methods and not bybit_method:
            print(bybit_methods)

        self.get_last_100 = self.db.query(models.WsCandle).order_by(models.WsCandle.id.desc()).limit(100).all()
        self.df = pd.DataFrame(columns=['Open', 'High', 'Low', 'Close', 'Volume'])

        for cndl in self.get_last_100:

            data = pd.DataFrame.from_dict({
                    'Open': [cndl.open],
                    'High': [cndl.high],
                    'Low': [cndl.low],
                    'Close': [cndl.close],
                    'Volume': [cndl.volume]
                }
            )

            self.df = pd.concat([self.df, data], ignore_index=True)


        # print(self.df)

   

    # Get 20 simple moving average
    def sma_20(self):
        print(self.bybit_method)

        # pop sma 20
        self.df['20sma'] = self.df['Close'].rolling(window=20).mean()

        # pop standart deviation
        self.df['stddev'] = self.df['Close'].rolling(window=20).std()
        
        # pop Bollinger Bands

        # BB lower line
        self.df['lower_band'] = self.df['20sma'] - (2 * self.df['stddev'])
        # BB upper line
        self.df['upper_band'] = self.df['20sma'] + (2 * self.df['stddev'])

        # Keltner Channel
        self.df['TR'] = abs(self.df['High'].astype(float) - self.df['Low'].astype(float))
        self.df['ATR'] = self.df['TR'].rolling(window=20).mean()

        self.df['lower_keltner'] = self.df['20sma'] - (self.df['ATR'] * 1.5)
        self.df['upper_keltner'] = self.df['20sma'] + (self.df['ATR'] * 1.5)

        print(self.df)
       
        