import os
import pandas as pd
import plotly.graph_objects as go
from bybit import ByBitMethods



class Indicators(ByBitMethods):

    def __init__(self, bybit_method=None):
        self.bybit_method = bybit_method


    def sma_20(self):
        print(self.bybit_method)
        print('done')
        


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