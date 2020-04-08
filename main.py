import pandas as pd
import ta
import requests
import time
import hmac
import hashlib
import base64

trade_type = 1

API_Key = 'YAu1qHdYPY906fmE5GQCdaQ0HnZTRbddjhXvanJEMvXYe2AuoQomTakVk6TbnVR6'
Secret_Key = ''


def binance_buy_call():
    global  trade_type
    trade_type=0

    header = {'X-MBX-APIKEY': API_Key}
    url = 'https://api.binance.com/api/v3/order'

    symbol = 'BTCUSDT'
    side = 'BUY'
    type = 'MARKET'
    quoteOrderQty = 11.0
    recvWindow = '5000'
    timestamp = str(time.time())

    message = 'symbol=BTCUSDT&side=BUY&type=MARKET&quoteOrderQty=11.0&recvWindow=5000&timestamp=' + timestamp

    signature = hmac.new(bytes(Secret_Key, 'latin-1'), msg=bytes(message, 'latin-1'),
                         digestmod=hashlib.sha256).hexdigest().upper()
    print(signature)
    params = 'symbol=BTCUSDT&side=BUY&type=MARKET&quoteOrderQty=12.0&recvWindow=5000&timestamp=' + timestamp + '&signature=' + signature
    print(params)
    order_status = requests.post(url,headers=header,params= params)

    print(order_status.text)



def binance_sell_call():

    global trade_type
    trade_type = 1

    header = {'X-MBX-APIKEY': API_Key}
    url = 'https://api.binance.com/api/v3/order'

    symbol = 'BTCUSDT'
    side = 'SELL'
    type = 'MARKET'
    quoteOrderQty = 11.0
    recvWindow = '5000'
    timestamp = str(round(time.time())*1000)
    print(timestamp)

    message = 'symbol=BTCUSDT&side=SELL&type=MARKET&quoteOrderQty=11.0&recvWindow=5000&timestamp='+timestamp

    signature = hmac.new(bytes(Secret_Key, 'latin-1'), msg=bytes(message, 'latin-1'),
                         digestmod=hashlib.sha256).hexdigest().upper()
    print(signature)
    params = 'symbol=BTCUSDT&side=SELL&type=MARKET&quoteOrderQty=12.0&recvWindow=5000&timestamp='+timestamp+'&signature='+signature
    print(params)
    order_status = requests.post(url,headers=header,params= params)

    print(order_status.json())

def stratergy(df,type):

    ma4 = ta.trend.SMAIndicator(close=df["Close"],n=4)
    ma9 = ta.trend.SMAIndicator(close=df["Close"],n=9)

    ma4_value = ma4.sma_indicator()[999]
    ma9_value = ma9.sma_indicator()[999]
    print("MA4 Value : ",ma4_value)
    print("MA9 Value : ", ma9_value)
    if type == 1 and ma4_value > ma9_value:  # buy = 1
        if (ma4_value-ma9_value) > 10:

            print("Called binance Buy function")
            binance_buy_call()

    if type == 0  and ma4_value < ma9_value:  # sell = 0
        print("Called binance Sell function")
        binance_sell_call()


def trade():
    while(1):
        data = requests.get('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=1000')

        df = pd.DataFrame(eval(data.text))

        df.columns = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume',
                      'Number of trades', 'tbbav', 'tbqav', 'ignore']

        global trade_type

        stratergy(df,trade_type)

        time.sleep(60)





trade()
