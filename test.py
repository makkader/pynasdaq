import pynasdaq as nas
import time
s = time.time()

print(nas.dividendCalendar("2019-10-15"))
# print(nas.highYieldDividendStocks())
# print(nas.dividendHistory("AAPL"))
# print(nas.stockSummaryQuote("MSB"))
# print(nas.currentPrice("AMZN"))
# print(nas.historicalStockQuote("aapl", "5d"))
#print(nas.flashQuotes(["TSLA", "RELL", "AAPL"]))
# print(nas.companyList("nyse"))
print("ELP ", (time.time()-s)/10)
