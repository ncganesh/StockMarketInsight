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

import re
from textblob import TextBlob



import json

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import requests




def get_coin_data(crypto='AMZN', start_date='2013-04-28', end_date=datetime.now(), save_data=None):
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



data=[]
def get_articles(urls):
    for url in urls:
        try:
            article = Article(url)
            article.download()
            article.parse()
            #article.nlp()
            print(url,article.title)
            data.append([article.publish_date,article.title,url])
        except:
            print('BAD URL')
            continue
    return pd.DataFrame(data)


def yahoonewsheadlines(option):
    print('Getting news data for ',option)
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (option, option)
    print('Getting news headlines and url from yahoo news data')
    latestheadlines,links = get_news_headlines(url)
    #print(df)
    return latestheadlines


def yahoonewsdata(option):
    print('Getting news data for ',option)
    url = "https://finance.yahoo.com/quote/%s/?p=%s" % (option, option)
    print('Getting news headlines and url from yahoo news data')
    latestheadlines,links = get_news_headlines(url)
    print('Getting news headlines and url from yahoo news data')
    df = get_articles(links[0:15])
    df.columns = ['date','title','url']
    df.drop_duplicates(subset="title", inplace=True)
    df = df.sort_values(by = ['date'],ascending=False)
    print('Extracted news articles')
    #print(df)
    return df


def clean_tweet(tweet):
	return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
	analysis = TextBlob(clean_tweet(tweet))
		# set sentiment
	if analysis.sentiment.polarity > 0:
		return 'positive'
	elif analysis.sentiment.polarity == 0:
		return 'neutral'
	else:
		return 'negative'

def getstocktwitsdata(option):
    url = "https://api.stocktwits.com/api/2/streams/symbol/%s.json?limit=200"%(option)
    #url = "https://api.stocktwits.com/api/2/streams/symbol/" + ticker + ".json"
    response = requests.get(url)
    data = json.loads(response.text)
    stocktwitsdata = pd.DataFrame(data['messages'])
    stocktwitsdata.time_UTC = pd.to_datetime(stocktwitsdata.created_at)
    stocktwitsdata['created_at'] = stocktwitsdata.time_UTC.dt.tz_convert('US/Eastern')
    stocktwitsdata['sentiment'] = [get_tweet_sentiment(tweet) for tweet in stocktwitsdata['body']]
    return stocktwitsdata



