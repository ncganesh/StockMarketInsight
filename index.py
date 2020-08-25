#from app import app
#from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from datetime import datetime
import dash_table
import pandas as pd
from data import yahoonewsdata,get_coin_data,getstocktwitsdata,yahoonewsheadlines
from data import *
import newspaper
import plotly.graph_objs as go
import nltk
import string, re
from collections import Counter
import dash


external_stylesheets = ['assets/bootsrap.css']
app = dash.Dash('Retail Technology Research Stock Analysis Dashboard',external_stylesheets = external_stylesheets)
server = app.server
app.config.suppress_callback_exceptions = True

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')


colors = {
    'background': '#000000',
    'background2': '#6533FF',
    'text': 'lightblue'
    }



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

stockgraph = [
    dbc.CardBody(
        dcc.Graph( id='graph-output')
         #html.Div(id='graph-output')

    )
]


stocktwitsgraph = [
    dbc.CardBody(
        dcc.Graph( id='stocktwits-graphoutput')
         #html.Div(id='stocktwits-graphoutput')

    )
]



'''
fig_treemap_all = treemap_wordcloudplot(tree_data)


fig_treemap_plot = [
    #dbc.CardHeader(html.H5("What three words or phrases would describe how you feel about E2E?")),
    dbc.CardBody(
        [
            dcc.Graph( id='fig_treemap_all',figure=fig_treemap_all)
            ,
        ],
    )
]

'''

app.layout = html.Div([
html.H1('Retail Innovation Center Stock Analysis Dashboard',
                               style={
                                      'textAlign': 'center',
                                      "background": "green"}),
dbc.Row(
            [
dcc.DatePickerRange(
                   id='date-input',
                   stay_open_on_select=False,
                   min_date_allowed=datetime(2014, 8, 10),
                   max_date_allowed=datetime.now(),
                   initial_visible_month=datetime.now(),
                   start_date=datetime(2020, 8, 13),
                   end_date=datetime.now(),
                   number_of_months_shown=2,
                   month_format='MMMM,YYYY',
                   display_format='YYYY-MM-DD',
                   style={
                          'color': '#11ff3b',
                          'font-size': '15px',
                          'margin': 10,
                          'padding': '8px',
                          'background': 'lightblue',
                   }
               ),

dcc.Input(id='dropdown', value='AMZN',
                                   type='search',
                            style={
                                'height': '50px',
                                'font-weight': 100,
                                'font-size': '16px',
                                'line-height': '10px',
                                'color': 'gray',
                                'margin': 0,
                                'padding': '8px',
                                'background': 'lightblue',
                                'position': 'middle',
                                'display': 'inline-block',
                                'width': '150px',
                                'vertical-align': 'middle'

                                }
                            ),
]),

html.H1("Stock Price on selected Ticker",style={
                                      'textAlign': 'center',"background": "#DBA21F"}),


dbc.Row(
            [
                dbc.Col(dbc.Card(stockgraph), style={"height" : "55%", "width" : "70%"},width= 5),
               #dbc.Col(dbc.Card(fig_treemap_plot),style={"height" : "55%", "width" : "70%"},width= 7),
           ],style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),

html.Div(style={"border":"2px black solid"}),
html.H1("Users Tweet on Selected Ticker",style={
                                      'textAlign': 'center',"background": "#DBA21F"}),

#html.Br(),html.Br(),html.Br(),



html.Br(),

dbc.Row(
            [
                dbc.Col(dbc.Card(stocktwitsoutput_table), width= 11),
                #dbc.Col(dbc.Card(fig_q2b_avgrating_scatter_plot),width= 5)

            ], style={"marginTop": 30,"marginBottom": 30}, justify="around",
        ),

html.Div(style={"border":"2px black solid"}),

html.H1("Stock News Article Summary on selected Ticker",style={
                                      'textAlign': 'center',"background": "#DBA21F"}),


dbc.Row(
            [

                dbc.Col(dbc.Card(newsheadlines_table), width=11),
            ], style={"marginTop": 30,"marginBottom": 30},justify="around",
        ),

html.Div(style={"border":"2px black solid"}),



#dbc.Row(
#            [
#
#                dbc.Col(dbc.Card(newssummary_table), width=11),
#            ], style={"marginTop": 30,"marginBottom": 30},justify="around",
#        ),


    ],
)



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
            page_size=5,
            style_header={'backgroundColor': '#7DF180', 'fontWeight': 'bold', 'border': '1px solid black',
                          'font_size': '18px'},
            style_cell={'font_size': '20px', 'whiteSpace': 'normal',
                        'height': 'auto', 'padding': '15px', 'width': '350px'},
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
                 'textAlign': 'center'},
                {'if': {'column_id': 'sentiment'},
                 'width': '15%',
                 'textAlign': 'left'},
            ]
        )

    return filteredtable








@app.callback(Output('table-output1', 'children'),
              [Input('dropdown', 'value')])
def get_data_table3(option):
    latestheadlines = yahoonewsheadlines(option)
    #print('-----LATEST HEADLINES---------------')
    #print(latestheadlines)
    df2 = pd.DataFrame(latestheadlines,columns = ['StockNewsHeadlines','url'])
    #df = df2[['StockNewsHeadlines']]
    filtereddf = df2.copy()
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
            page_size=10,
            style_header={'backgroundColor': '#009EEA', 'fontWeight': 'bold', 'border': '1px solid black',
                          'font_size': '18px'},
            style_cell={'font_size': '13px', 'whiteSpace': 'normal',
                        'height': 'auto', 'padding': '15px'},
            #export_format='csv',
            export_format='csv',
            export_headers='display',
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(248, 248, 248)'
                },
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
             'textAlign': 'center'},
            {'if': {'column_id': 'sentiment'},
             'width': '15%',
             'textAlign': 'left'},
        ]

        )

    return filteredtable





@app.callback(Output('stocktwits-graphoutput', 'figure'),
              [Input('dropdown', 'value')])
def render_graph2(value):
    df2 = getstocktwitsdata(value)
    df = df2[['created_at', 'body', 'sentiment']]

    def remove_punct(text):
        text = "".join([char for char in text if char not in string.punctuation])
        text = re.sub('[0-9]+', '', text)
        return text

    stopword = nltk.corpus.stopwords.words('english')

    def tokenization(text):
        text = re.split('\W+', text)
        return text

    def remove_stopwords(text):
        text = [word for word in text if word not in stopword]
        return text


    df['Tweet_punct'] = df['body'].apply(lambda x: remove_punct(x))
    df['Tweet_tokenized'] = df['Tweet_punct'].apply(lambda x: tokenization(x.lower()))
    df['Tweet_nonstop'] = df['Tweet_tokenized'].apply(lambda x: remove_stopwords(x))

    lis = []
    for i in range(len(df)):
        lis.extend(df['Tweet_nonstop'][i])


    lis2 = Counter(lis)
    lis3 = lis2.most_common(15)

    data = [go.Bar(
        x=[i[0] for i in lis3],
        y=[i[1] for i in lis3],
        marker=dict(colorscale='Jet'
                    ),
        text='Word counts'
    )]
    return dcc.Graph(
        id='example-graph',
        figure={
            'data': data,
            'layout':
            go.Layout(title='Most Frequently Used Words by Users', barmode='stack')
        })




@app.callback(Output('graph-output', 'figure'),
              [Input('date-input', 'start_date'),
               Input('date-input', 'end_date'),
               Input('dropdown', 'value')])
def render_graph(start_date, end_date, option):
    df = get_coin_data(crypto=option, start_date=start_date, end_date=end_date, save_data=None)
    data = df[(df.date >= start_date) & (df.date <= end_date)]
    return dcc.Graph(
        id='graph-1',
        figure={
            'data': [
                {'x': data['date'], 'y': data['price'], 'type': 'line', 'name': 'value1'},
            ],
            'layout': {
                'title': 'Price Vs Time ',
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text'],
                    'size': 18
                },
                'xaxis': {
                        'title': 'Time',
                        'showspikes': True,
                        'spikedash': 'dot',
                        'spikemode': 'across',
                        'spikesnap': 'cursor',
                        },
                'yaxis': {
                        'title': 'Price',
                        'showspikes': True,
                        'spikedash': 'dot',
                        'spikemode': 'across',
                        'spikesnap': 'cursor'
                        },

            }
        }
    )

@app.callback(Output('table-output', 'children'),
              [Input('dropdown', 'value')])

def get_data_table(option):
    df2 = yahoonewsdata(option)
    #print('DF2', df2)
    # df2.columns = ['article.publish_date','article.title','url']
    # print('Index',df2)
    # df = pd.DataFrame(df2,columns = ['url','Headlines'])
    # print('Df Index',df)
    df = df2[['title', 'url',  'summary']]
    df.columns = ['StockNewsArticleTitle', 'url','Summarized Sentence using NLP']
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

        css=[
            {'selector': '.row-1', 'rule': 'background: #E6A000;'}
        ],


        page_size=5,
        style_header={'backgroundColor': '#7DF180', 'fontWeight': 'bold', 'border': '1px solid black',
                      'font_size': '18px'},
        style_cell={'font_size': '18px', 'whiteSpace': 'normal',
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
            {'if': {'column_id': 'StockNewsArticleTitle'},
             'width': '5%',
             'textAlign': 'left'},
            {'if': {'column_id': 'url'},
             'width': '5%',
             'textAlign': 'left'},
            {'if': {'column_id': 'Summarized Sentence using NLP'},
             'width': '90%',
             'textAlign': 'left'},

        ]

    )

    return filteredtable


if __name__ == '__main__':
    app.run_server(debug=True)
