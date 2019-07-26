import pandas as pd
import requests
from lxml import html, etree
from io import StringIO


from .common import DIVIDEND_CALENDAR_URL, HIGH_YIELD_DIVIDEND_URL, DIVIDEND_HISTORY_URL


def dividendCalendar(date=""):
    ''' Returns dividend calendar for NASDAQ.
    Args:
        date (string): in YYYY-Mmm-DD (e.g., 2019-Jan-01)

    returns: DataFrame
    '''
    response = requests.get(DIVIDEND_CALENDAR_URL, params={'date': date})
    docTree = html.fromstring(response.content)
    table = docTree.xpath('//table[@id="Table1"]')
    df = pd.read_html(etree.tostring(table[0]))

    return df[0]


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
    returns dividend history of a given symbol
    '''
    response = requests.get(DIVIDEND_HISTORY_URL.format(symbol=symbol))
    docTree = html.fromstring(response.content)
    table = docTree.xpath(
        '//table[@id="quotes_content_left_dividendhistoryGrid"]')
    df = pd.read_html(etree.tostring(table[0]))

    return df[0]
