import pynasdaq as nas
import time
s = time.time()

# print(nas.dividendCalendar("2019-09-13"))
# print(nas.highYieldDividendStocks())
print(nas.dividendHistory("AAPL"))
# print(nas.stockSummaryQuote("MSB"))
# print(nas.currentPrice("FB"))
# print(nas.historicalStockQuote("aapl", "5d"))
# print(nas.flashQuotes(["TSLA", "RELL", "AAPL"]))
# print(nas.companyList("nyse"))
# print(nas.getPressReleaseHeadlines("AAPL"))
# print(nas.getPressReleaseContent("https://www.nasdaq.com/press-release/apple-reports-third-quarter-results-20190730-01201"))
print("ELP ", (time.time()-s)/10)
