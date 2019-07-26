import pandas as pd
import requests
from lxml import html, etree
# from io import StringIO


from .common import STOCK_SUMMARY_QUOTE_URL


def stockSummaryQuote(symbol):
    response = requests.get(STOCK_SUMMARY_QUOTE_URL.format(symbol=symbol))
    docTree = html.fromstring(response.content)

    curPrice = docTree.xpath('//div[@id="qwidget_lastsale"]/text()')[0].strip()[1:]

    colspans = docTree.xpath(
        '//div[@class="row overview-results relativeP"]')
    tableRows = colspans[0].xpath('.//div[@class="table-row"]')

    data = {"Symbol": symbol, "CurrentPrice": curPrice}
    for row in tableRows:
        cells = row.xpath('./div[@class="table-cell"]')
        key = cells[0].xpath('./b/text()')[0].strip()
        val = cells[1].text.strip()
        data[key] = val

    return pd.DataFrame(data, index=[0])
