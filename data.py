import yfinance as yf
from datetime import datetime
# Get the data for the stock AAPL
from PriceIndices import Indices
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

#Imports
import time
#Assign time.time() object to "start" so we can profile the code.
start = time.time()
import pandas as pd
import numpy as np
from newspaper import Article

import json

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import requests




def get_coin_data(crypto='AMZN', start_date='2013-04-28', end_date='2020-04-28', save_data=None):
    df2 = yf.download(crypto, start_date, end_date)
    df2['Date'] = df2.index

    df = df2[['Date', 'Close']]
    df.columns = ['date', 'price']
    #print(df)
    df_bi = Indices.get_simple_moving_average(df)
    df_bi.drop('price', axis=1, inplace=True)


    df = pd.merge(df, df_bi, on='date', how='left')
    #print(df)
    del df_bi

    for col in df.columns[1:]:
        df[col] = np.round(df[col], 2)
    while save_data:
        df.to_csv('data.csv', index=False)
        break
    return df


def get_news_headlines(url):
    latestheadlines = []
    latestheadlines_links = []
    parsed_uri = urlparse.urljoin(url, '/')

    try:

        req = requests.get(url)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        html = soup.findAll('h3')
        links = soup.findAll('a')

        if html:
            for i in html:
                latestheadlines.append((i.next.next.next.next, url))

        if links:
            for i in links:
                if '/news/' in i['href']:
                    l = parsed_uri.rstrip('/') + i['href']

                    latestheadlines_links.append(l)


    except requests.exceptions.RequestException as re:
        print("Exception: can't crawl web site (%s)" % re)
        pass

    return latestheadlines, latestheadlines_links

def get_articles(links):
    # Intialize list articles_info list
    articles_info = []
    for i in links:
        # Intialize dictionary
        article_dict = {}
        # Insert link "i" into the dictionary
        article_dict["link"] = i
        # Pass link into Article() function
        art = Article(i)
        # Download contents of art object
        art.download()

        # Try/except is included because not all articles can be parsed
        try:
            # If article can be successfully parsed then insert its text, title, publish_date, keywords
            # and summary into corresponding keys
            art.parse()
            article_dict["text"] = art.text
            article_dict["title"] = art.title
            article_dict["date"] = art.publish_date
            art.nlp()
            article_dict["keywords"] = art.keywords
            article_dict["summary"] = art.summary
        except newspaper.article.ArticleException:
            # If article cannot be parse then insert null values for the following keys:
            # "text", "title", "date", "keywords", and "summary"
            article_dict["text"] = np.nan
            article_dict["title"] = np.nan
            article_dict["date"] = np.nan
            article_dict["keywords"] = np.nan
            article_dict["summary"] = np.nan

        # Insert dictionary of article info into the articles_info list
        articles_info.append(article_dict)
    # Pass the list of dictionaries into a pandas data frame
    corpus = pd.DataFrame(articles_info)
    # Print how long the process took
    print("Script took {:.2f} seconds to complete".format(time.time() - start))
    return corpus


def yahoonewsdata(option):
    print('Getting news data for ',option)
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (option, option)
    latestheadlines,links = get_news_headlines(url)
    #df = get_articles(links)
    return latestheadlines

def getstocktwitsdata(option):
    url = "https://api.stocktwits.com/api/2/streams/symbol/%s.json?limit=200"%(option)
    #url = "https://api.stocktwits.com/api/2/streams/symbol/" + ticker + ".json"
    response = requests.get(url)
    data = json.loads(response.text)
    stocktwitsdata = pd.DataFrame(data['messages'])
    return stocktwitsdata



