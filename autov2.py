import time
import pyupbit
import datetime
import numpy as np

access = ""
secret = ""


def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=8)
    target_price = df.iloc[7]['close'] + (df.iloc[7]['high'] - df.iloc[7]['low']
                                          +df.iloc[6]['high'] - df.iloc[6]['low']
                                          +df.iloc[5]['high'] - df.iloc[5]['low']
                                          +df.iloc[4]['high'] - df.iloc[4]['low']
                                          +df.iloc[3]['high'] - df.iloc[3]['low']
                                          +df.iloc[2]['high'] - df.iloc[2]['low']
                                          +df.iloc[1]['high'] - df.iloc[1]['low']
                                          +df.iloc[0]['high'] - df.iloc[0]['low'])/7 * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC")
        end_time = start_time + datetime.timedelta(days=1)

        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 1.3)
            current_price = get_current_price("KRW-BTC")
            if target_price < current_price:
                krw = get_balance("KRW")
                if krw > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
        else:
            btc = get_balance("BTC")
            if btc > 0.00008:
                upbit.sell_market_order("KRW-BTC", btc)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)