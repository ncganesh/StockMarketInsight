import yfinance as yf
from datetime import datetime
# Get the data for the stock AAPL
from PriceIndices import Indices
from bs4 import BeautifulSoup




import nltk # the Natural Language Toolkit, used for preprocessing
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string

#Imports
import time
#Assign time.time() object to "start" so we can profile the code.
start = time.time()
import pandas as pd
import numpy as np
from newspaper import Article

import re
from textblob import TextBlob


from sklearn.feature_extraction.text import CountVectorizer

import json

try:
    import urllib.parse as urlparse
except ImportError:
    import urlparse
import requests




def get_coin_data(crypto, start_date, end_date):
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
            article.nlp()
           #print(url,article.title,article.text)
            data.append([article.publish_date,article.title,url,article.text,article.summary])

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
    df = get_articles(links)
    #print(df)
    df.columns = ['date','title','url','text','summary']
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
    print("MESSSAGES")
    #print(data)
    stocktwitsdata = pd.DataFrame(data['messages'])
    stocktwitsdata.time_UTC = pd.to_datetime(stocktwitsdata.created_at)
    stocktwitsdata['created_at'] = stocktwitsdata.time_UTC.dt.tz_convert('US/Eastern')
    stocktwitsdata["date"] = [d.date() for d in stocktwitsdata["created_at"]]
    stocktwitsdata["time"] = [d.time() for d in stocktwitsdata["created_at"]]
    stocktwitsdata['sentiment'] = [get_tweet_sentiment(tweet) for tweet in stocktwitsdata['body']]
    return stocktwitsdata


def text_lowercase(text):
    return text.lower()
# remove numbers
def remove_numbers(text):
    result = re.sub(r'\d+', '', text)
    return result
# remove punctuation
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
# tokenize
def tokenize(text):
    text = word_tokenize(text)
    return text
# remove stopwords
stop_words = set(stopwords.words('english'))
def remove_stopwords(text):
    text = [i for i in text if not i in stop_words]
    return text
# lemmatize
lemmatizer = WordNetLemmatizer()
def lemmatize(text):
    text = [lemmatizer.lemmatize(token) for token in text]
    return text

def preprocessing(text):
    text = text_lowercase(text)
    text = text.replace('\n',' ')
    text = remove_numbers(text)
    text = remove_punctuation(text)
    text = tokenize(text)
    text = remove_stopwords(text)
    text = lemmatize(text)
    text2 = ' '.join(text)
    return text2


def preprocesstextcol_getcounts(data,colname):
    #data2 = preprocessdata(data)
    data2 = data.copy()
    text = data2[colname].apply(lambda x: preprocessing(str(x)))
    text2 = ' '.join(text)
    data_c3 = pd.Series([word for word in str(text2).split(' ') if len(word)>3])
    #df_col_valcnt = data_c3.value_counts(normalize = True).mul(100).round(1).rename_axis('words').to_frame('percentages')
    #df_col_valcnt = df.sort_values(by = 'percentages')
    words_withcount = data_c3.value_counts().rename_axis('words').reset_index(name='counts')
    words_withcount['counts'] = words_withcount['counts'].astype('category')
    topwords_withcount = words_withcount.head(10)
    return words_withcount,topwords_withcount

import pandas as pd
import plotly.graph_objects as go

import plotly.express as px
def treemap_wordcloudplot(tree_data):
    fig = px.treemap(tree_data, path=["column", "words"], values='counts')
    fig.update_layout(
        #margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            size=25,
            # color="RebeccaPurple"
        )
    )
    return fig




def get_top_n_bigram(corpus, ngramvalue,n):
    vec = CountVectorizer(ngram_range=(ngramvalue, ngramvalue)).fit(corpus)
    bag_of_words = vec.transform(corpus)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
    words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
    return words_freq[:n]



def get_ngramcounts(data,colname,ngramvalue,n):
    text = data[colname].apply(lambda x: preprocessing(str(x)))
    common_words = get_top_n_bigram(text, ngramvalue,n)
    words_withcount =  pd.DataFrame(common_words, columns = ['words' , 'counts'])
    words_withcount['counts'] = words_withcount['counts'].astype('category')
    topwords_withcount = words_withcount.head(n)
    return topwords_withcount

def ngram_plot(data,colname,ngramvalue,n,title):
    topwords_withcount = get_ngramcounts(data,colname,ngramvalue,n)
    y = topwords_withcount.words
    x = topwords_withcount.counts
    trace1 = go.Bar(y = y, x = x,orientation='h',marker = dict(color='#009EEA'),text = y)
    data = [trace1]
    layout = go.Layout(barmode = "group",title=title, xaxis= dict(title='Counts'),yaxis=dict(autorange="reversed"),showlegend=False,font=dict(size=15),width = 350)
    fig = go.Figure(data = data, layout = layout)
    return fig




def pie_dropdownall(sentvalues, colors1):
    labels = ["positive","neutral","negative"]
    values = list(sentvalues)
    fig =go.Figure(data=[go.Pie(labels=labels, values=values,marker=dict(colors=colors1, line=dict(color='#070707', width=1)))])
    fig.update_layout(
        # margin=dict(l=20, r=20, t=20, b=20),
        font=dict(
            size=17,
            # color="RebeccaPurple"
        ),
        width = 400,
    )
    return fig
