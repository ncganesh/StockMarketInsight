# RICSA-StockMarketInsight

The Dashboard is avilable at https://retailstocknews.herokuapp.com/

Visual Analytics Platform that helps the users  to easily get information about any Selected  company ,

How they are performing and their Historical Stock Price?

How Users are reacting to company at that time?

News Headlines of the Company.

Get All Related News Articles on selected Ticker  and Summarized News using NLP in one table.

Corelate  News  Headlines and User tweets to see  users are tweeting more about some news and their Sentiments.

Steps to execute :

Package Required:

nltk==3.4.5

pandas==0.24.2

plotly==4.1.1

dash_html_components==1.0.1

dash==1.3.0

yfinance==0.1.54

dash_table==4.3.0

newspaper3k==0.2.8

dash_core_components==1.2.0

textblob==0.15.3

requests==2.22.0

beautifulsoup4==4.9.1

numpy==1.18.4

PriceIndices==1.1.1

gunicorn==20.0.4


1. Install python requirements using pip : 

pip install -r requirements.txt


2. python index.py

3. Dash Dashboard will be available at - http://127.0.0.1:8050/




## Real Time Stock Price Data from Yahoo Finance API

yf.download(tickername, start_date, end_date)

## Stock Twits is a platform where  actual investors and traders tweet in real time about the stocks.

## Summarizing News Article using NLP








