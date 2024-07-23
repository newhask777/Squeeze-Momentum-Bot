import os, pandas
import plotly.graph_objects as go
from plotly.offline import iplot


symbols = ['AAPL']

for filename in os.listdir('datasets'):
    # print(filename)
    symbol = filename.split(".")[0]
    # print(symbol)
    df = pandas.read_csv('datasets/{}'.format(filename))
    # print(df)
    if df.empty:
        continue


    # Simple Moving avg
    df['20sma'] = df['Close'].rolling(window=20).mean()

    # Standart deviation
    df['stddev'] = df['Close'].rolling(window=20).std()

    # BB lower line
    df['lower_band'] = df['20sma'] - (2 * df['stddev'])
    # BB upper line
    df['upper_band'] = df['20sma'] + (2 * df['stddev'])


    # Keltner Channel
    df['TR'] = abs(df['High'] - df['Low'])
    df['ATR'] = df['TR'].rolling(window=20).mean()

    df['lower_keltner'] = df['20sma'] - (df['ATR'] * 1.5)
    df['upper_keltner'] = df['20sma'] + (df['ATR'] * 1.5)


    def in_squeeze(df):
        return df['lower_band'] > df['lower_keltner'] and df['upper_band'] < df['upper_keltner']
    
    df['squeeze_on'] = df.apply(in_squeeze, axis=1)

    if df.iloc[-1]['squeeze_on']:
        print("{} is in the squeeze".format(symbol))
    



#     if symbol in symbols:
#         print(df)
#         aapl_df = df

# candlestick = go.Candlestick(x=df['Date'], open=aapl_df['Open'], high=aapl_df['High'], low=aapl_df['Low'], close=aapl_df['Close'])
# upper_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_band'], name='Upper Bollinger Band', line={'color': 'red'})
# lower_band = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_band'], name='Lower Bollinger Band', line={'color': 'red'})
# upper_keltner = go.Scatter(x=aapl_df['Date'], y=aapl_df['upper_keltner'], name='Upper Ketlner Channel', line={'color': 'blue'})
# lower_keltner = go.Scatter(x=aapl_df['Date'], y=aapl_df['lower_keltner'], name='Lower Ketlner Channel', line={'color': 'blue'})

# fig = go.Figure(data=[candlestick, upper_band, lower_band])
# fig.layout.xaxis.type = 'category'
# fig.layout.xaxis.rangeslider.visible = False

# fig.show()