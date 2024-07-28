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
    


    # Get 20 sma
    def sma_20(self):
        print(self.bybit_method)
        
       
        


    def standart_deviation():
        pass

    def bb_lower(sma, std):
        pass

    def bb_upper(sma, std):
        pass

    def tr():
        pass

    def atr():
        pass

    def lower_keltner():
        pass

    def upper_keltner():
        pass