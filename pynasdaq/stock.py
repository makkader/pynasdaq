import pandas as pd
import requests
from lxml import html, etree
from io import StringIO


from .common import STOCK_SUMMARY_QUOTE_URL, HISTORICAL_STOCK_URL, FLASH_QUOTE_URL, INFO_QUOTE_URL


def currentPrice(symbol):

    # response = requests.get(STOCK_SUMMARY_QUOTE_URL.format(symbol=symbol))
    # docTree = html.fromstring(response.content)
    # curPrice = float(docTree.xpath('(//div[@id="qwidget_lastsale"])[1]/text()')[0].strip()[1:])

    response = requests.get(INFO_QUOTE_URL, params={"symbol": symbol})
    docTree = html.fromstring(response.text)
    priceStr = docTree.xpath('(//span[@class="lastsale_qn"])[1]/label[1]/text()')[0]
    priceStr = priceStr.strip()[1:].replace(',', "")
    curPrice = float(priceStr)

    data = {"Symbol": symbol, "CurrentPrice": curPrice}

    return pd.DataFrame(data, index=[0])


def stockSummaryQuote(symbol):
    response = requests.get(STOCK_SUMMARY_QUOTE_URL.format(symbol=symbol))
    docTree = html.fromstring(response.content)

    curPrice = float(docTree.xpath(
        '//div[@id="qwidget_lastsale"]/text()')[0].strip()[1:])

    colspans = docTree.xpath(
        '//div[@class="row overview-results relativeP"]')
    tableRows = colspans[0].xpath('.//div[@class="table-row"]')

    data = {"Symbol": symbol, "CurrentPrice": curPrice}
    for row in tableRows:
        cells = row.xpath('./div[@class="table-cell"]')
        key = cells[0].xpath('./b/text()')[0].strip()
        valStr = cells[1].text.strip()
        if key == "Previous Close" or key == "Annualized Dividend" or key == "Earnings Per Share (EPS)":
            val = float(cells[1].text.strip()[1:])
        elif key == "1 Year Target" or key == "P/E Ratio" or key == "Forward P/E (1y)" or key == "Beta":

            val = 0 if valStr == "" else float(valStr)

        elif key == "Market Cap" or key == "Share Volume" or key == "50 Day Avg. Daily Volume":
            val = int(cells[1].text.strip().replace(",", ""))
        else:
            val = cells[1].text.strip()
        data[key] = val

    return pd.DataFrame(data, index=[0])


def historicalStockQuote(symbol, timeframe="1m"):
    payload = "{timeframe}|true".format(timeframe=timeframe)
    headers = {'Content-Type': "application/json"}
    url = HISTORICAL_STOCK_URL.format(symbol=symbol.lower())

    response = requests.post(url, data=payload, headers=headers)
    return pd.read_csv(StringIO(response.text), index_col=False)


def flashQuotes(symbolList):

    headers = {
        'cookie': "userSymbolList="+'&'.join(symbolList)
    }
    response = requests.request("GET", FLASH_QUOTE_URL,  headers=headers)
    docTree = html.fromstring(response.content)
    table = docTree.xpath('(//div[@class="genTable"])[1]/table')[0]

    head = [th.strip() for th in table.xpath('.//th/a/text()[1]|.//th[@align]/text()')]
    head.insert(3, "ChangeDirection")

    rows = table.xpath(".//tr[@class]")
    dic = []
    for r in rows:
        datarow = {}
        for i, c in enumerate(r.xpath('./td//text()')):
            datarow[head[i]] = c.strip()
        dic.append(datarow)
    df = pd.DataFrame(dic, columns=head)

    def convert2num(x):
        x = x.replace('$', '').replace(',', '').replace('%', '')
        return float(x)

    df[['Last Sale', 'Change', '% Change', 'Share Volume']] = df[[
        'Last Sale', 'Change', '% Change', 'Share Volume']].applymap(convert2num)
    return df
