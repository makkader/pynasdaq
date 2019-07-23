import pandas as pd
import requests
from lxml import html, etree

from .common import DIVIDEND_CALENDAR_URL


def dividendCalendar(date=""):
    ''' Returns dividend calendar for NASDAQ.
    Args:
        date (string): in YYYY-Mmm-DD (e.g., 2019-Jan-01)

    returns: DataFrame
    '''
    response = requests.get(DIVIDEND_CALENDAR_URL+"?date="+date)
    docTree = html.fromstring(response.content)
    table = docTree.xpath('//table[@id="Table1"]')
    df = pd.read_html(etree.tostring(table[0]))

    return df[0]
