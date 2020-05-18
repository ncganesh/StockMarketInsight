# RICSA-StockMarketInsight

The Dashboard is avilable at https://retailstocknews.herokuapp.com/

Visual Analytics Platform that helps the users  to easily get information about any Selected  Ticker ,

How they are performing and their Historical Stock Price?
How Users are reacting to company at that time?
News Headlines of the Company.
Get All Related News Articles on selected Ticker  and Summarized News using NLP in one table.
Corelate  News  Headlines and User tweets to see  users are tweeting more about some news and their Sentiments.



-----------------------------------------------------------------------------------------------------------------------------------
Steps to execute :



1. Install python requirements using pip : 

pip install -r requirements.txt


2. python index.py

3. Dash Dashboard will be available at - http://127.0.0.1:8050/


----------------------------------------------------------------------------------------------------------------------------------

 Real Time Stock Price Data from Yahoo Finance API

yf.download(tickername, start_date, end_date)

Stock Twits is a platform where  actual investors and traders tweet in real time about the stocks and get data in real time.

Getting Stock Twits  Data in realtime.

Summarizing News Article using NLP



-----------------------------------------------------------------------------------------------------------------------------------



CHALLENGES

Text Summarization using Deep Learning(BART) and other Summarization method used  takes some  time to display summarized article on Dashboard.

Getting Stock Twits  Data through requests module has a limit of 30 tweets. 


FUTURE WORK

Get data through Stock Twits API’S and save all data in Database so that we can see the historical sentiment trend.

Collect the Historical data from News Articles and build a Semantic News Article Search Engine to search the  historical relevant articles based on User’s Search.

----------------------------------------------------------------------------------------------------------------------------------------

