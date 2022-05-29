from os import curdir
from symtable import Symbol
import time
import ccxt
import datetime
from numpy import short
import pandas as pd
api_key = '6zHOZK1HIAidFdxoGxHR5GB85VOqCZ7VbbKXdBz8Ne6XfFUG4feKcPfVw15o0Ew1'
secret = 'PevYip6CONYhgYKdNTVnGjIYGS03hptq09jqUgsCUlLFlJJXJ7KcTXUyGmJmEVcl'
binance = ccxt.binance(config={
    'apiKey': api_key, 
    'secret': secret,
    'enableRateLimit': False,
    'options': {
        'defaultType': 'future'
    }
})

def cal_target(self,coin,origin):
   try: 
    btc = binance.fetch_ohlcv(
        symbol=coin,
        timeframe='1d', 
        since=None, 
        limit=10)
    df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
    df.set_index('datetime', inplace=True)
    yesterday = df.iloc[-2]
    today = df.iloc[-1]
    long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
    short_target = today['open'] - (yesterday['high'] - yesterday['low']) * 0.5
    if origin == 'long':
     return long_target
    if origin == 'short':
     return short_target 
    if origin == False:
     return today['open']
   except Exception as e:
     print(e,"3")
def cal_amount(usdt_balance, cur_price):
   try: 
    amount = ((usdt_balance * 1000000)/cur_price) / 1000000
    return amount 
   except Exception as e:
     None
amount_list = []
type = []
cur_price_list = []
def enter_position(exchange, coin, cur_price,long_target, coin_amount, position,bought_coin):
   if position['type'] == 'long': 
    if (long_target * 1.01 >=cur_price >= long_target): 
        coin2 = coin.replace("/","")
        binance.fapiPrivate_post_leverage({  
            'symbol': coin2,  
            'leverage': position['leverege'],  
        })
        exchange.create_market_buy_order(
            symbol= coin, 
            amount= coin_amount * position['leverege'],             
            params={'type': 'future'})
        cur_price_list.append(cur_price)
        amount_list.append(coin_amount)
        bought_coin.append(coin)  
        print("지구 롱")
        print(len(bought_coin),coin,a * "_",usdt,b * "_",cur_price,c * "_",coin_amount)
   if position['type'] == 'short': 
    if long_target * 1.05 >= cur_price >= long_target: 
        coin2 = coin.replace("/","")
        binance.fapiPrivate_post_leverage({  
            'symbol': coin2,  
            'leverage': position['leverege'],  
        })
        exchange.create_market_sell_order(
            symbol= coin, 
            amount= coin_amount * position['leverege'],             
            params={'type': 'future'})
        cur_price_list.append(cur_price)
        bought_coin.append(coin)  
        amount_list.append(coin_amount)
        print("지구 숏")
        print(len(bought_coin),coin,a * "_",usdt,b * "_",cur_price,c * "_",coin_amount)
def exit_position(exchange,i):
    amount = amount_list[i]
    coin = bought_coin[i]
    if position['type']  == 'short':
        exchange.create_market_buy_order(symbol=coin, amount=amount)
        bought_coin[i] = ""
        amount_list[i] = 0
    if position['type']  == 'long':
        exchange.create_market_sell_order(symbol=coin, amount=amount)
        bought_coin[i] = ""
        amount_list[i] = 0
coin = ""
start = False
markets = binance.load_markets() 
long_target = [0 for i in markets.keys()]
short_target = [0 for i in markets.keys()]
position = {"leverege":5,"type":"short"} 
bought_coin = []
m =0
op_mode = True
k = 1
long_up = 0
long_down = 0
up_average = 20
per_average = 0.5
while True: 
  try:
    now = datetime.datetime.now()                     
    markets = binance.load_markets()  
    n = 0
    for i in markets.keys():
      if 'USDT' in i: 
          n = n + 1  
    Market= ["" for i in range(n)]
    n = 0
    for i in markets.keys():
       if 'USDT' in i: 
        Market[n] = i
        n = n + 1
    if m < len(Market):                                               
        coin = Market[m]                             
        if k == 0:
            if op_mode:
                for i in range(len(bought_coin)):
                 if amount_list[i] != 0
                  exit_position(binance,i)
                  print("팔기")
                n = 0
                markets = binance.load_markets()
                for i in markets.keys():
                    if 'USDT' in i: 
                        n = n + 1  
                    
                Market= ["" for i in range(n)]
                n = 0
                for i in markets.keys():
                    if 'USDT' in i: 
                        Market[n] = i
                        n = n + 1
                a = 0
                n = 0
                per_average = 0
                up_average = 0
                up_list = []
                now = datetime.datetime.now() 
                while a < 99:
                 a = a + 1
                 try:
                  for i in Market:
                   btc = binance.fetch_ohlcv(
                        symbol=i,
                        timeframe='1d', 
                        since=None, 
                        limit=100)
                   df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                   df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                   df.set_index('datetime', inplace=True)
                   yesterday = df.iloc[a - 1]
                   today = df.iloc[a] 
                   long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
                   if today['high'] > long_target:
                      up_list.append(i)
                   #print(up_list) 
                  up = 0
                  down = 0
                  per = 0
                  for i in up_list:
                   btc = binance.fetch_ohlcv(
                        symbol=i,
                        timeframe='1d', 
                        since=None, 
                        limit=100)
                   df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                   df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                   df.set_index('datetime', inplace=True)
                   yesterday = df.iloc[a - 1]
                   today = df.iloc[a] 
                   long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
                   if today['close'] > long_target:
                    per = (per + today['close'] / long_target) 
                    #print(i,"상승",today['close'] / long_target)
                    up = up + 1
                   else:
                    per = (per + today['close'] / long_target)
                    #print(i,"하강",today['close'] / long_target) 
                    down = down + 1
                  now = now - datetime.timedelta(days = 1)
                  print(now,len(up_list),up,down,per/len(up_list))
                  per_average = per_average + per/len(up_list)
                  up_average = up_average + len(up_list)
                  up = 0
                  down = 0
                  up_list = []
                 except Exception as e:
                  per_average = per_average/(a-1)
                  up_average = 20
                  break
                if per_average > 1:
                    position['type'] = 'long'
                else:
                    position['type'] = 'short'
                op_mode = False
                bought_coin = []
                cur_price_list = []
                type = []
                amount_list = []
                start = False
                long_target = [0 for i in markets.keys()]
                k = 1
        elif now.hour == 9 and now.minute == 00 and (0 <= now.second < 10):
            if op_mode:
                for i in range(len(bought_coin)):
                 exit_position(binance,i)
                n = 0
                markets = binance.load_markets()
                for i in markets.keys():
                    if 'USDT' in i: 
                        n = n + 1  
                    
                Market= ["" for i in range(n)]
                n = 0
                for i in markets.keys():
                    if 'USDT' in i: 
                        Market[n] = i
                        n = n + 1
                a = 0
                n = 0
                per_average = 0
                up_average = 0
                up_list = []
                now = datetime.datetime.now() 
                while a < 99:
                 a = a + 1
                 try:
                  for i in Market:
                   btc = binance.fetch_ohlcv(
                        symbol=i,
                        timeframe='1d', 
                        since=None, 
                        limit=100)
                   df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                   df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                   df.set_index('datetime', inplace=True)
                   yesterday = df.iloc[a - 1]
                   today = df.iloc[a] 
                   long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
                   if today['high'] > long_target:
                      up_list.append(i)
                   #print(up_list) 
                  up = 0
                  down = 0
                  per = 0
                  for i in up_list:
                   btc = binance.fetch_ohlcv(
                        symbol=i,
                        timeframe='1d', 
                        since=None, 
                        limit=100)
                   df = pd.DataFrame(data=btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                   df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
                   df.set_index('datetime', inplace=True)
                   yesterday = df.iloc[a - 1]
                   today = df.iloc[a] 
                   long_target = today['open'] + (yesterday['high'] - yesterday['low']) * 0.5
                   if today['close'] > long_target:
                    per = (per + today['close'] / long_target) 
                    #print(i,"상승",today['close'] / long_target)
                    up = up + 1
                   else:
                    per = (per + today['close'] / long_target)
                    #print(i,"하강",today['close'] / long_target) 
                    down = down + 1
                  now = now - datetime.timedelta(days = 1)
                  print(now,len(up_list),up,down,per/len(up_list))
                  per_average = per_average + per/len(up_list)
                  up_average = up_average + len(up_list)
                  up = 0
                  down = 0
                  up_list = []
                 except Exception as e:
                  per_average = per_average/(a-1)
                  up_average = 20
                  break
                if per_average > 1:
                    position['type'] = 'long'
                else:
                    position['type'] = 'short'
                op_mode = False
                bought_coin = []
                cur_price_list = []
                type = []
                amount_list = []
                start = False
                long_target = [0 for i in markets.keys()]
        if start == False :               
            start = True
            balance = binance.fetch_balance()        
            usdt = balance['total']['USDT']
        if start:
         if long_target[m]  == 0:
          long = 'long'
          long_target[m] = cal_target(binance,coin,long)
         op_mode = True
         ticker = binance.fetch_ticker(coin)
         cur_price = ticker['last']              
         if op_mode and len(bought_coin) < round(up_average) and now.hour >= 9 and coin not in bought_coin: 
            amount = cal_amount(usdt/round(up_average), cur_price)
            a = 16- len(coin)
            b = 11 - len(str(usdt))
            c = 11 - len(str(cur_price))
            d = 25 - len(str(long_target[m]))
            enter_position(binance, coin, cur_price,long_target[m],amount, position,bought_coin)
         if op_mode and len(bought_coin) >= 1:
          for i in range(len(bought_coin)):
           if amount_list[i] != 0
            ticker = binance.fetch_ticker(bought_coin[i])
            cur_price = ticker['last']
            if position['type'] == 'long':
                if cur_price <= (cur_price_list[i]) * 0.9:
                   exit_position(binance, i)
                   print("돔황차")
                   print(usdt)
                if cur_price >= (cur_price_list[i]) * 1.1:
                   exit_position(binance, i) 
                   print("익절")
                   print(usdt)
            if position['type'] == 'short':
                if cur_price >= (cur_price_list[i]) * 1.1:
                   exit_position(binance ,i)
                   print("돔황차")
                   print(usdt)
                if cur_price <= (cur_price_list[i]) * 0.9:
                   exit_position(binance, i) 
                   print("익절")
                   print(usdt)
            time.sleep(0.1)
        time.sleep(0.1)
        m = m + 1
    else:
        m = 0
  except Exception as e:
      m = m + 1   
     
