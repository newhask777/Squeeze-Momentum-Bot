import os
import pandas as pd
import plotly.graph_objects as go
from bybit import ByBitMethods


class Indicators(ByBitMethods):

    def __init__(self, bybit_method, *args, **kwargs):
        super(Indicators, self).__init__(*args, **kwargs)
        self.bybit_method = bybit_method

        if self.bybit_method == 'websocket':
            print(self.bybit_method)
            self.ws_stream()
            

        elif self.bybit_method[0] == 'http':
            print(self.bybit_method)
            print('http')
            self.http_query


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