import os
import pandas as pd
import plotly.graph_objects as go
from bybit import ByBitMethods

from db import models
from datetime import datetime
import time



class Indicators(ByBitMethods):


    def __init__(self, bybit_method: str, bybit_methods: dict=None, *args, **kwargs):
        super(Indicators, self).__init__(*args, **kwargs)
        self.bybit_method = bybit_method


    # Get 20 simple moving average
    def sma_20(self):
        print(self.bybit_method)
        

        if self.bybit_method == 'websocket':

            self.ws_stream()

            self.get_last_100 = self.db.query(models.WsCandle).order_by(models.WsCandle.stamp.asc()).limit(100).all()
            # self.get_last_100 = self.db.query(models.WsCandle).order_by(models.WsCandle.id.desc()).limit(100).all()
            self.df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

            for cndl in self.get_last_100:

                data = pd.DataFrame.from_dict({
                        'Date': [cndl.stamp],
                        'Open': [cndl.open],
                        'High': [cndl.high],
                        'Low': [cndl.low],
                        'Close': [cndl.close],
                        'Volume': [cndl.volume]
                    }
                )

                self.df = pd.concat([self.df, data], ignore_index=True)



        if self.bybit_method == 'http':

            self.http_query()
             
            self.get_last_100 = self.db.query(models.HttpCandle).order_by(models.HttpCandle.id.asc()).limit(100).all()
            self.df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume'])

            for cndl in self.get_last_100:

                data = pd.DataFrame.from_dict({
                        'Date': [cndl.stamp],
                        'Open': [cndl.open],
                        'High': [cndl.high],
                        'Low': [cndl.low],
                        'Close': [cndl.close],
                        'Volume': [cndl.volume]
                    }
                )


                self.df = pd.concat([self.df, data], ignore_index=True)         
        # print(self.df)

        self.df['20sma'] = self.df['Close'].rolling(window=20).mean()
        self.df['stddev'] = self.df['Close'].rolling(window=20).std()
        self.df['lower_band'] = self.df['20sma'] - (2 * self.df['stddev'])
        self.df['upper_band'] = self.df['20sma'] + (2 * self.df['stddev'])

        self.df['TR'] = abs(self.df['High'].astype(float) - self.df['Low'].astype(float))
        self.df['ATR'] = self.df['TR'].rolling(window=20).mean()

        self.df['lower_keltner'] = self.df['20sma'] - (self.df['ATR'] * 1.5)
        self.df['upper_keltner'] = self.df['20sma'] + (self.df['ATR'] * 1.5)

    
        # self.df = self.df.iloc[::-1]
        print(self.df)

        self.plot_symbol()
        

        # if self.df[(self.df['lower_band'] > self.df['lower_keltner']) & (self.df['upper_band'] < self.df['upper_keltner'])]:
        #     print('Up')



    def plot_symbol(self):
        candlestick = go.Candlestick(x=self.df['Date'], open=self.df['Open'], high=self.df['High'], low=self.df['Low'], close=self.df['Close'])
        upper_band = go.Scatter(x=self.df['Date'], y=self.df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
        lower_band = go.Scatter(x=self.df['Date'], y=self.df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})
        upper_keltner = go.Scatter(x=self.df['Date'], y=self.df['upper_keltner'], name='Upper Ketlner Channel', line={'color': 'blue'})
        lower_keltner = go.Scatter(x=self.df['Date'], y=self.df['lower_keltner'], name='Lower Ketlner Channel', line={'color': 'blue'})

        fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_keltner, lower_keltner])
        fig.layout.xaxis.type = 'category'
        fig.layout.xaxis.rangeslider.visible = False

        fig.show()
       
        

