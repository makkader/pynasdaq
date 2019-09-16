import pandas as pd
import requests
from lxml import html, etree
from io import StringIO


from .common import INFO_API, BATCH_QUOTE_API, COMPANY_LIST_URL, CHART_API


def currentPrice(symbol):
    '''
    Arg: A symbol
    Returns: DataSeries
    '''

    response = requests.get(CHART_API.format(symbol))
    data = response.json()['data']
    price = float(data['lastSalePrice'].replace(',', "").replace('$', ''))
    return pd.Series({'symbol': data['symbol'], 'company': data['company'], 'lastSalePrice': price})


def stockSummaryQuote(symbol):
    '''
    Arg: A symbol
    Returns: DataFrame with summary quote. All field type string
    '''
    response = requests.get(INFO_API.format(symbol))
    data = response.json()['data']
    keystats = data['keyStats']
    return pd.Series({'symbol': data['symbol'], 'company': data['companyName'], 'lastSalePrice': data['primaryData']['lastSalePrice'],
                      'volume': keystats['Volume']['value'], "MarketCap": keystats['MarketCap']['value']})


def historicalStockQuote(symbol, fromdate, todate):

    params = {'fromdate': fromdate, 'todate': todate}
    response = requests.get(CHART_API.format(symbol), params=params)
    data = response.json()['data']['chart']

    df = pd.DataFrame.from_dict(map(lambda x: x['z'], data))
    return df


def miniBatchQuotes(symbolList):
    '''
    Args: a symbol list - number of symbols must be less than or equal 20
    Return: df with string column type
    '''
   # ?symbol=aapl|stocks&symbol=goog|stocks

    url = BATCH_QUOTE_API+"?"+'&'.join(map(lambda s: "symbol={}|stocks".format(s), symbolList))
    response = requests.request("GET", url)
    data = response.json()['data']
    df = pd.DataFrame.from_dict(data)
    return df


def batchQuotes(symbolList):
    '''
    Args: a symbol list - number of symbols
    Return: df with string column type
    '''
    qlist = []
    for i in range(0, len(symbolList), 20):
        qlist.append(miniBatchQuotes(symbolList[i:i+20]))
    df = pd.concat(qlist).set_index("symbol")
    return df


def companyList(exchange="nyse"):
    '''
    Arg: An exchange name. Possible values are ["nasdaq","nyse","amex"]. Default: nasdaq.
    Return: Dataframe of list of companies
    '''
    exchange = exchange.lower()
    if exchange not in ["nasdaq", "nyse", "amex"]:
        return "Valid exchange names are nasdaq, nyse, and amex."
    url = COMPANY_LIST_URL.format(exchange=exchange)
    response = requests.get(url)
    return pd.read_csv(StringIO(response.text), index_col=0).drop(["Summary Quote", "Unnamed: 8"], axis=1)
