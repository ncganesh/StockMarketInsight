#from app import app
#from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_table
import pandas as pd
#from data import yahoonewsdata,get_coin_data,getstocktwitsdata,yahoonewsheadlines
from data import *
import newspaper
import plotly.graph_objs as go
import nltk
import string, re
from collections import Counter
import dash


primary_blue = '#0000A0'
secondary_yellow ='#E6A000'
light_blue = '#009FEB'
body_gray = '#707070'
accent_gray = '#F2F2F2'

mainheadline_color = '#06430C'
primary_color = '#064507'
main_color = '#E6A000'
secondary_color = '#1DAB2C'

external_stylesheets = ['assets/bootsrapnew.css']
#app = dash.Dash('Retail Technology Research Stock Analysis Dashboard',external_stylesheets = [dbc.themes.BOOTSTRAP])
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')


colors = {
    'background': '#000000',
    'background2': '#6533FF',
    'text': 'lightblue'
    }
NAVBAR = dbc.Navbar(
    children=[
        dbc.Row(
            [

                html.H1([html.Span("Retail Innovation Center ", style={'color':light_blue}), html.Span("Stock Analysis Dashboard", style={'color':'white'})], className='ml-3'),
            ],
            align="center",
            no_gutters=True,
        ),
    ],
    color=mainheadline_color,
    dark=True,
    sticky="top"
)



stocktwitsoutput_table = [
    dbc.CardBody(
        html.Label(id='stocktwits-output')

    )
]


newsheadlines_table = [
    dbc.CardBody(
        html.Label(id='table-output')

    )
]


newssummary_table = [
    dbc.CardBody(
        html.Label(id='table-output1')

    )
]


stocktwitsgraph = [
    dbc.CardBody(
        dcc.Graph( id='stocktwits-graphoutput')
         #html.Div(id='stocktwits-graphoutput')

    )
]

fig_treemap_plot = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='fig_treemap_all')
            ,
        ],
    )
]


YAHOONEWS_bigramplot = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='yahoonewsbigramplot')
            ,
        ],
    )
]






sentimentpiestocktwits_fig = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
  dcc.Graph( id='sentimentpiestocktwits')
            ,

]

yahoonewsunigramplot_fig = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='yahoonewsunigramplot')
            ,
        ],
    )
]


stockwitsunigramplot_fig = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),

            dcc.Graph( id='stockwitsunigramplot')
            ,

]



sentimentpieyahoonews_fig = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='yahoonews_pie')
            ,
        ],
    )
]

STOCKTWITS_bigramplot =  [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='stockwitsbigramplot')
            ,
        ],
    )
]



LINE_GRAPH =  [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='graph-output')
            ,
        ],
    )
]





STOCKTWITS_UNIGRAM_PIE_PLOT = [
    dbc.Col(
        [
            dbc.Row(stockwitsunigramplot_fig),
            dbc.Row(sentimentpiestocktwits_fig),
        ],
    ),
]



YAHOONEWS_UNIGRAM_PIE_PLOT = [
    dbc.Row(
        [
            dbc.Col(yahoonewsunigramplot_fig),
            dbc.Col(sentimentpieyahoonews_fig),
        ],
    ),
]


BODY = html.Div([
'-- SELECT DATES --',
dcc.DatePickerRange(
                   id='date-input',
                   start_date='2020-05-15',
                   end_date= '2020-08-31',
                   style={
                          'color': secondary_color,
                          'font-size': '15px',
                          'margin': 10,
                          'padding': '8px',
                            'textAlign' :  'center',
                          'background': '#009EEA',
                   }
               ),
               ' ---  SELECT TICKER ---',
                dcc.Input(id='dropdown', value='AAPL',
                                   type='search',
                            style={
                                'height': '50px',
                                'font-weight': 100,
                                'font-size': '16px',
                                'line-height': '10px',
                                'margin': 0,
                                'padding': '8px',
                                'background': '#009EEA',
                                'position': 'middle',
                                'display': 'inline-block',
                                'textAlign' :  'center',
                                'width': '150px',
                                'vertical-align': 'middle'

                                }
                            ),






html.Div(style={"border":"2px black solid"}),


html.H1("Stock Price on Selected Ticker",style={
                                      'textAlign': 'center',"background": secondary_color}),
dbc.Row(
            [
                dbc.Col(dbc.Card(LINE_GRAPH), md= 7)

            ], style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),

html.Br(),

#dbc.Row(dbc.Col(dbc.Card(stockgraph),width=8), style={"marginTop": 30},justify="around"),
html.H1("Users Tweet on Selected Ticker",style={
                                      'textAlign': 'center',"background": secondary_color}),

#html.Br(),html.Br(),html.Br(),




dbc.Row(
            [
                dbc.Col(dbc.Card(stocktwitsoutput_table), md= 6),
                dbc.Col(dbc.Card(STOCKTWITS_UNIGRAM_PIE_PLOT), md=4.5)

            ], style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),


html.Div(style={"border":"2px black solid"}),
html.H1("StockTwits and News Article Corelation ",style={
                                      'textAlign': 'center',"background": secondary_color}),

#dbc.Row(dbc.Col(dbc.Card(fig_treemap_plot),width=8), style={"marginTop": 30},justify="around"),
dbc.Row(
            [
                dbc.Col(dbc.Card(STOCKTWITS_bigramplot ), md= 5),
                dbc.Col(dbc.Card(YAHOONEWS_bigramplot), md=5)

            ], style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),


html.Div(style={"border":"2px black solid"}),

html.H1("Stock News Article Summary on selected Ticker",style={
                                      'textAlign': 'center',"background": secondary_color}),


dbc.Row(
            [
                dbc.Col(dbc.Card(newsheadlines_table), lg=10),
                dbc.Row(dbc.Card(YAHOONEWS_UNIGRAM_PIE_PLOT))

            ], style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),


html.Div(style={"border":"2px black solid"}),




    ],
)


app.layout = html.Div([NAVBAR,BODY])



@app.callback(Output('stocktwits-output', 'children'),
              [Input('dropdown', 'value')])
def get_data_table2(option):
    df2 = getstocktwitsdata(option)
    #print('---STOCKTWITS---')
    #print(df2)
    df = df2[['date','time','body','sentiment']]
    df.columns = ['UserTweetDate', 'Time', 'Tweet', 'sentiment']

    filtereddf = df.copy()
    filteredtable = dash_table.DataTable(

            id='datatable-output',
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'lineHeight': '15px'
            },

            data=filtereddf.to_dict('records'),

            filter_action='native',


            css=[
                { 'selector': '.row-1', 'rule': 'background: #E6A000;' }
            ],
            columns=[{'id': c, 'name': c} for c in filtereddf.columns],
            page_size=8,
            style_header={'backgroundColor': main_color, 'fontWeight': 'bold', 'border': '1px solid black',
                          'font_size': '18px'},
            style_cell={'font_size': '11px', 'font_family':"Arial",'whiteSpace': 'normal',
                        'height': 'auto', 'padding': '15px'

                        },
            #export_format='csv',
            export_format='csv',
            export_headers='display',
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                }
            ],
            style_cell_conditional=[
                {'if': {'column_id': 'UserTweetDate'},
                 'width': '10%',
                 'textAlign': 'center'},
                {'if': {'column_id': 'Time'},
                 'width': '10%',
                 'textAlign': 'center'},
                {'if': {'column_id': 'Tweet'},
                 'width': '55%',
                 'textAlign': 'left'},
                {'if': {'column_id': 'sentiment'},
                 'width': '15%',
                 'textAlign': 'left'},
            ]
        )

    return filteredtable






@app.callback(Output('graph-output', 'figure'),
              [Input('dropdown', 'value'),
                  Input('date-input', 'start_date'),
               Input('date-input', 'end_date')
               ])
def render_graph(value,start_date, end_date):
    df = get_coin_data(value, start_date, end_date)
    data = df[(df.index >= start_date) & (df.index <= end_date)]
    print("STOCK DATA")
    #print(data)
    fig = get_stockgraph(data)
    return fig


@app.callback(Output('table-output', 'children'),
              [Input('dropdown', 'value')])

def get_data_table(option):
    df2 = yahoonewsdata(option)
    #print('DF2', df2)
    # df2.columns = ['article.publish_date','article.title','url']
    # print('Index',df2)
    # df = pd.DataFrame(df2,columns = ['url','Headlines'])
    # print('Df Index',df)
    df = df2[['date','title', 'url',  'summary']]
    df['date'] = df['date'].dt.date
    print(df.dtypes)
    df.columns = ['Date','StockNewsArticleTitle', 'URL','Summarized Sentence using NLP']
    filtereddf = df.copy()
    filteredtable = dash_table.DataTable(

        id='datatable-output',
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },

        data=filtereddf.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in filtereddf.columns],
        #columns=[{'name': 'Link', 'id': 'Link', 'type': 'text', 'presentation': 'markdown'}],

        filter_action='native',
        sort_action = 'native',
        style_table={'overflowY': 'auto', 'maxHeight': 500},
        css=[
            {'selector': '.row-1', 'rule': 'background: #E6A000;'}
        ],


        page_size=5,
        style_header={'backgroundColor': main_color, 'fontWeight': 'bold', 'border': '1px solid black',
                      'font_size': '18px'},
        style_cell={'font_size': '15px', 'font_family':"Arial",'whiteSpace': 'normal',
                    'height': 'auto', 'padding': '15px'},
        # export_format='csv',
        export_format='csv',
        # style_data_conditional=[
        #    {
        #        'if': {'row_index': 'odd'},
        #        'backgroundColor': 'rgb(248, 248, 248)'
        #    }
        # ],
        style_cell_conditional=[
            {'if': {'column_id': 'Date'},
             'width': '10%',
             'textAlign': 'left'},
            {'if': {'column_id': 'StockNewsArticleTitle'},
             'width': '7%',
             'textAlign': 'left'},
            {'if': {'column_id': 'URL'},
             'width': '7%',
             'textAlign': 'left'},
            {'if': {'column_id': 'Summarized Sentence using NLP'},
             'width': '75%',
             'textAlign': 'left'},

        ]

    )

    return filteredtable


@app.callback(
    [
    Output('yahoonewsbigramplot', 'figure'),
    Output('yahoonewsunigramplot', 'figure'),
    Output('yahoonews_pie', 'figure')
     ],
    [Input('dropdown', 'value')]
    )

def update_dropdown(value):
        title =  '<b> News Article Bigrams</b>'
        ngramvalue = 2
        n = 3
        yahoonewsdf = yahoonewsdata(value)
        yahoonews_df = yahoonewsdf[['title', 'url', 'text', 'summary']]
        fig = ngram_plot(yahoonews_df, 'text', ngramvalue, n, title)

        title2 = value + ' <b> News Article Unigrams</b>'
        uningramvalue = 1
        n = 5
        fig2 = ngram_plot(yahoonews_df, 'text', uningramvalue, n, title2)
        colors1 = ['rgb(0, 0, 160)', 'rgb(230, 160, 0)', 'rgb(0, 158,234)']
        yahoonews_df['sentiment'] = [get_tweet_sentiment(tweet) for tweet in yahoonews_df['text']]
        stcounts = yahoonews_df['sentiment'].value_counts().rename_axis('sentiments_st').to_frame(
            'counts')
        print(stcounts['counts'])
        # print(df_stocktwits)
        print("Plotting PIE")
        title = "<b>Sentiment Distributions from News Articles<b>"
        fig3 = pie_dropdownall(stcounts['counts'], colors1,title)
        return fig,fig2,fig3




@app.callback(
    [
    Output('stockwitsbigramplot', 'figure'),
    Output('stockwitsunigramplot', 'figure'),
     Output('sentimentpiestocktwits', 'figure')],
    [Input('dropdown', 'value')]
    )

def update_dropdown(value):
    title = value + '<b> Stock Twits Bigrams</b>'
    ngramvalue = 2
    n = 5
    stocktwitsdf = getstocktwitsdata(value)
    df_stocktwits = stocktwitsdf[['created_at', 'body', 'sentiment']]
    fig = ngram_plot(df_stocktwits, 'body', ngramvalue, n, title)


    ngramvalue = 1
    title ="<b>Most used words for </b>" +  value
    n = 5
    fig2 = ngram_plot(df_stocktwits, 'body', ngramvalue, n, title)

    colors1 = ['rgb(0, 0, 160)', 'rgb(230, 160, 0)', 'rgb(0, 158,234)']
    stcounts = df_stocktwits['sentiment'].value_counts().rename_axis('sentiments_st').to_frame(
        'counts')
    print(stcounts['counts'])
    # print(df_stocktwits)
    print("Plotting PIE")
    title = "<b>Sentiment Distributions from Stock Twits</b>"
    fig3 = pie_dropdownall(stcounts['counts'], colors1,title)

    return fig,fig2,fig3

@app.callback(
    Output('fig_treemap_all', 'figure'),
    [Input('dropdown', 'value')]
    )

def update_treemap(value):
    print("Getting Data for plotting Treemap")
    df2 = getstocktwitsdata(value)
    df_stocktwits = df2[['created_at', 'body', 'sentiment']]
    df2 = yahoonewsdata(value)
    df_yahoonews = df2[['title', 'url','text' ,'summary']]
    colname = 'text'
    topwords_withcount = get_ngramcounts(df_yahoonews,colname,2,5)
    topwords_withcount['column'] = 'YahooNews'
    colname = 'body'
    topwords_withcount1 = get_ngramcounts(df_stocktwits,colname,2,5)
    topwords_withcount1['column'] = 'StockTwits'
    tree_data = pd.concat([topwords_withcount,topwords_withcount1])
    print("Tree map data updated")

    fig_treemap_all = treemap_wordcloudplot(tree_data)
    return fig_treemap_all

if __name__ == '__main__':
    app.run_server(debug=True)


