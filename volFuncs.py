import requests
import pandas as pd
import numpy as np
import datetime
from numpy import mean
import time
import math
import plotly.express as px
from datetime import datetime
from datetime import date
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st


##################################################################
#create venv -- python3 -m venv env
#run venv --  .\env\Scripts\activate
# leave venv -- deactivate 
##################################################################


def cryptowatchAPIcall(option, then, now):
    #now = str(int(time.time()))
    #then = '1483261261'
    exchange = "coinbase-pro"   
    params = {
        "after": then,
        "before": now,
        "periods": 86400,
    }
    pricefeed = requests.get(
    f'https://api.cryptowat.ch/markets/{exchange}/{option}/ohlc',
    params=params)
    crypto_price = pricefeed.json()
    return crypto_price

def to_date(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime('%m/%d/%Y')

def json_to_df(cryptowat):
    funcinput = cryptowat
    day_count = len(funcinput["result"]["86400"])
    #print(f"Retrieving historical prices for {option}")
    print(f'Analyzing {day_count} total days')
    daily_resp = funcinput["result"]["86400"]
    O =[] 
    H=[]
    L=[]
    C=[]
    vol=[]
    date=[]
    weekday=[]
    new_date = []
    count = 0
    
    #populate all lists from json response
    while count < day_count:
        date.append(daily_resp[count][0])
        O.append(daily_resp[count][1])
        H.append(daily_resp[count][2])
        L.append(daily_resp[count][3])
        C.append(daily_resp[count][4])
        vol.append(daily_resp[count][5])
        if count > day_count:
            break
        count = count + 1
    
        
    #convert unix date to readable date
    for x in date:
        new = to_date(x)
        new_date.append(new)
        
    #create DataFrame    
    df = pd.DataFrame()
    df["Date"] = new_date
    df["Open"] = O
    df["High"] = H
    df["Low"] = L
    df["Close"] = C
    df["Volume"] = vol
    df["log_return"] = np.log(df.Close) - np.log(df.Close.shift(1))
    # df.set_index(["Date"])
    return df    

def RollingVolCrypto(crypto):
    #calculate Vol
    st_dev = crypto['log_return'].std()
    print(f'The Average vol for any given day is {st_dev}')
    volatility = crypto['log_return'].std()*365**.5
    print(f'{volatility} vol asset in the given period')
    crypto['weekly_vol'] = crypto['log_return'].rolling(window=7).std()*7**.5
    
    fig = px.histogram(crypto, x=crypto["Date"], y=crypto["weekly_vol"], title='Weekly Rolling Volatility')
    fig.update_xaxes(
        dtick=150,
        tickformat="%b")
    fig.update_layout(
        title = "Weekly Rolling Volatility",
        template="plotly_dark")
    #fig.show()
    
    return fig


def DAILYavgVol(crypto):
    st_dev = crypto['log_return'].std()
    st_dev = "{:.0%}".format(st_dev)
    return st_dev


def VolScore(crypto):
    volatility = crypto['log_return'].std()*365**.5
    volatility =  "{:.0%}".format(volatility)

    return volatility


def logLinechart(crypto):
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    # Add traces
    fig.add_trace(
        go.Scatter(x=crypto["Date"], y=crypto['log_return']),
        secondary_y=False)
    fig.update_xaxes(
        dtick=150,
        tickformat="%b")
    fig.update_layout(
        title = "Logarithmic Returns",
        template="simple_white")
    
    return fig

# function to return key for any value
def get_key(val):
    for key, value in projectdict.items():
         if val == value:
             return key

projectdict = {
    "ethusd":"Ethereum",
    "btcusd":"Bitcoin",
    "adausd":"Cardano",
    "dogeusd":"DogeCoin",
    "dotusd":"PolkaDot",
    "avaxusd":"Avalanche",
    "solusd":"Solana",
   "ltcusd":"Litecoin",
    "zecusd":"Zcash"
}


def RollingVolCrypto_MONTH(crypto):
    #calculate Vol
    st_dev = crypto['log_return'].std()
    print(f'The Average vol for any given week is {st_dev}')
    volatility = crypto['log_return'].std()*52**.5
    print(f'{volatility} vol asset in the given period')
    crypto['monthly_vol'] = crypto['log_return'].rolling(window=4).std()*7**.5
    
    fig = px.histogram(crypto, x=crypto["Date"], y=crypto["monthly_vol"], title='Monthly Rolling Volatility',
                 labels={
                     "monthly_vol": " Monthly Volatility"
                 })
    fig.update_xaxes(
        dtick=50,
        tickformat="%B %Y")
    fig.update_yaxes(
        tickformat="%")
    fig.update_layout(
        title = "Average Volatility",
        template="simple_white")
    #fig.show()
    
    return fig

def json_to_df_WEEK(cryptowat):
    funcinput = cryptowat
    day_count = len(funcinput["result"]["604800"])
    #print(f"Retrieving historical prices for {option}")
    print(f'Analyzing {day_count} total days')
    daily_resp = funcinput["result"]["604800"]
    O =[] 
    H=[]
    L=[]
    C=[]
    vol=[]
    date=[]
    weekday=[]
    new_date = []
    count = 0
    
    #populate all lists from json response
    while count < day_count:
        date.append(daily_resp[count][0])
        O.append(daily_resp[count][1])
        H.append(daily_resp[count][2])
        L.append(daily_resp[count][3])
        C.append(daily_resp[count][4])
        vol.append(daily_resp[count][5])
        if count > day_count:
            break
        count = count + 1
    
        
    #convert unix date to readable date
    for x in date:
        new = to_date(x)
        new_date.append(new)
        
    #create DataFrame    
    df = pd.DataFrame()
    df["Date"] = new_date
    df["Open"] = O
    df["High"] = H
    df["Low"] = L
    df["Close"] = C
    df["Volume"] = vol
    df["log_return"] = np.log(df.Close) - np.log(df.Close.shift(1))
    # df.set_index(["Date"])
    return df
    

def cryptowatchAPIcallWEEK(option, then, now):
    #now = str(int(time.time()))
   # then = '1483261261'
    exchange = "coinbase-pro"  
    params = {
        "after": then,
        "before": now,
        "periods": 604800,
    }
    pricefeed = requests.get(
    f'https://api.cryptowat.ch/markets/{exchange}/{option}/ohlc',
    params=params)
    crypto_price = pricefeed.json()
    return crypto_price


def histologs(crypto):
    #crypto["Volume"] = crypto['Volume']
    fig = px.histogram(crypto, y = crypto["Volume"], x=crypto["Date"], title ="Volume",
                      labels={
                          "sum of Volume": "Volume in USD ($)",
                          "Date": "  "
                      })
    fig.update_xaxes(
        dtick=50,
        tickformat="%B %Y")
    fig.update_layout(
        title = "Volume",
        template="simple_white")
    
    return fig


def lineChart(crypto):
    fig3 = px.line(crypto, y =crypto["Close"], x = crypto["Date"], labels = {
        "Close": "Price USD ($)",
        "Date": "   "
    })
    fig3.update_xaxes(
        dtick=50,
        tickformat = "%B %Y")
    fig3.update_yaxes(
        type = 'log')
    fig3.update_layout(
        title = "Price",
        template ="simple_white",
        height=600)
    return fig3


def to_timestamp(dateString):
    #element = datetime.strptime(dateString, '%m/%d/%Y')
    element = date.strftime(dateString, '%Y/%m/%d')
    element = datetime.strptime(element, '%Y/%m/%d')

    return int(datetime.timestamp(element))


def daycount(cryptowat):
    funcinput = cryptowat
    day_count = len(funcinput["result"]["86400"])

    return day_count