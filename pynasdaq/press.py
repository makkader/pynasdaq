from .common import FLASH_QUOTE_URL
import pandas as pd
import requests
from lxml import html, etree
from io import StringIO
from datetime import datetime


PRESS_RELEASE_URL = "https://www.nasdaq.com/symbol/{}/press-releases"
PRESS_RELEASE_PRINT_URL = "https://www.nasdaq.com/aspx/stockmarketnewsstoryprint.aspx?storyid={}"


def getPressReleaseHeadlines(symbol):

    response = requests.request("GET", PRESS_RELEASE_URL.format(symbol))
    docTree = html.fromstring(response.content)
    newsDivs = docTree.xpath('(//div[@class="news-headlines"])[1]/div[not(@id) and not(@class)]')

    allnews = []
    for news in newsDivs:
        title = news.xpath('./span/a/text()')[0]
        link = news.xpath('./span/a/@href')[0]
        dateAndNewsSource = news.xpath('./small/text()')[0].strip()
        datestr, newssrc = dateAndNewsSource.split("-")
        date = datetime.strptime(datestr.strip(), '%m/%d/%Y %I:%M:%S %p')
        allnews.append({"title": title, "link": link, "date": date, "src": newssrc})
    return pd.DataFrame(allnews)


def getPressReleaseContent(newsLink):
    storyid = newsLink.split('/')[-1]
    response = requests.request("GET", PRESS_RELEASE_PRINT_URL.format(storyid))
    return response.text
