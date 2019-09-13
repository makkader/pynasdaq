import pandas as pd
import requests
from lxml import html, etree
from io import StringIO


from .common import DIVIDEND_CALENDAR_URL, HIGH_YIELD_DIVIDEND_URL, DIVIDEND_HISTORY_API


def dividendCalendar(date=""):
    ''' Returns dividend calendar for NASDAQ.
    Args:
        date (string): in YYYY-MM-DD (e.g., 2019-09-01)

    returns: DataFrame or None
    '''
    response = requests.get(DIVIDEND_CALENDAR_URL, params={'date': date})
    rows = response.json()['data']['calendar']['rows']
    if rows is not None:
        return pd.DataFrame.from_dict(rows)


def highYieldDividendStocks():
    '''
    returns: pandas DataFrame of high yield dividend stocks
    '''
    response = requests.get(HIGH_YIELD_DIVIDEND_URL)
    df = pd.read_csv(StringIO(response.text),
                     index_col=False).set_index("Symbol")
    return df.sort_values(by=['dividendyield'], ascending=False)


def dividendHistory(symbol):
    '''
    returns: Dataframe or None for the dividend history of a given symbol 
    '''
    response = requests.get(DIVIDEND_HISTORY_API.format(symbol=symbol))

    rows = response.json()['data']['dividends']['rows']
    if rows is not None:
        return pd.DataFrame.from_dict(rows)
