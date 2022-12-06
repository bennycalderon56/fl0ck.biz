# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from urllib.request import urlopen
import json
#import talib
#import yfinance as yf
#import pandas as pd
#import pandas_datareader as web
#from backtesting import Backtest, Strategy
#from backtesting.lib import crossover
#from backtesting.test import SMA
#import datetime as dt
#import matplotlib.pyplot as plt


def get_all():
    gains = get_gains()
    loss = get_loss()
    active = get_active()
    news = get_news()
    #etf = get_etfH()

    data = {
         "winners":gains,
         "active":active,
         "losers":loss,
         "newsfeed": news,
         "segment": 'index'
         #"etf":etf
    }
    return data



def index(request):
    
    data = get_all()
    context = data
    #context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))
    #return render(request,'templates/home/index.html',{context})


def pages(request):
    # Activenews = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/stock_news?limit=1&apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")
    # tTitle = json_extract(Activenews,'title')
    # tSite = json_extract(Activenews,'url')
    # news = dict(zip(tTitle,tSite))
    #context = {"newsfeed":news}
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def get_gains():
    Movergain = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/stock/gainers?apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")
    #GAINS 
    tickerGain = json_extract(Movergain,'ticker')
    tGainPer = json_extract(Movergain,'changesPercentage')
    gains = dict(zip(tickerGain,tGainPer))
    return gains

def get_loss():
    Moverloss = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/stock/losers?apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")
    #LOSSES
    tickerLoss = json_extract(Moverloss,'ticker')
    tLossPer = json_extract(Moverloss,'changesPercentage')
    loss = dict(zip(tickerLoss,tLossPer))
    return loss

def get_active():
    Moveractive = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/stock/actives?apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")
    #ACTIVE
    tickerActive = json_extract(Moveractive,'ticker')
    tActive = json_extract(Moveractive,'changes')
    active = dict(zip(tickerActive,tActive))
    return active

def get_etfH():
    etf = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/etf-holder/SPY?apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")
    #ACTIVE
    ticker = json_extract(etf,'asset')
    name = json_extract(etf,'name')
    price = json_extract(etf,'marketValue')
    active = dict(zip(name,price))
    return active


def get_news():
    Activenews = get_jsonparsed_data("https://financialmodelingprep.com/api/v3/stock_news?limit=30&apikey=2a4bf570d78de5dea1ca8e7e1e6244c0")  
    #NEWS
    tTitle = json_extract(Activenews,'title')
    tText = json_extract(Activenews,'text')
    tSite = json_extract(Activenews,'url')
    
    news = list(zip(tTitle,tText,tSite))
    return news




def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)

def json_extract(obj,key):
    arr = []
    def extract(obj,arr,key):
        if isinstance(obj,dict):
            for k,v in obj.items():
                if isinstance(v,(dict,list)):
                    extract(v,arr,key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj,list):
            for item in obj:
                extract(item,arr,key)
        return arr
    values = extract(obj,arr,key)
    return values