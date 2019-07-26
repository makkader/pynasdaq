import pynasdaq as nas
#print(nas.dividendCalendar("2019-Jul-29"))
# print(nas.highYieldDividendStocks())
# print(nas.dividendHistory("AAPL"))
# print(nas.stockSummaryQuote("MSB"))
# print(nas.currentPrice("MSB"))
print(nas.historicalStockQuote("aapl", "5d"))
