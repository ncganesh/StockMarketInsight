from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
from data import yahoonewsdata,get_coin_data,getstocktwitsdata,yahoonewsheadlines
import newspaper
import plotly.graph_objs as go
import nltk
import string, re
from collections import Counter
stopwords = nltk.corpus.stopwords.words('english')


colors = {
    'background': '#000000',
    'background2': '#6533FF',
    'text': 'lightblue'
    }
coin_list = ['AMZN','WMT','COST','KR']


app.layout = html.Div([html.H1('Retail Innovation Center Stock Analysis Dashboard',
                               style={
                                      'textAlign': 'center',
                                      "background": "green"}),

               ' ---|---',
               html.Div(['Select Dates to view Historical Trend ',
               dcc.DatePickerRange(
                   id='date-input',
                   stay_open_on_select=False,
                   min_date_allowed=datetime(2013, 4, 28),
                   max_date_allowed=datetime.now(),
                   initial_visible_month=datetime.now(),
                   start_date=datetime(2019, 1, 1),
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
               ' ---|--- Select Ticker here',
                dcc.Input(id='dropdown', value='WMT',
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
                html.Div(id='date-output'),
                html.Div(id='intermediate-value', style={'display': 'none'}),
                               ], className="row ",
                    style={'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'white',
                           'display': 'inline-block'}),

                html.Div([
                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                    dcc.Tab(label='Stock Price on selected Ticker', value='tab-1',style={'textAlign': 'center','font-size': '32px',"background": "lightblue"}),
                    dcc.Tab(label='Stock News Headlines on selected Ticker', value='tab-2',style={'textAlign': 'center','font-size': '32px',"background": "lightblue"}),
                ]),
                html.Div(id='tabs-example-content')
                ]),


               html.Div(children=[dcc.Markdown(" Retail Tech")], style={'textAlign': 'center',"background": "green"}),
                              ],
              style={"background": "#6533FF"}
                            )

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([

            #html.Div(className='row', children=[html.Div(id='graph-output', className='col s12 m6 l6'),
             #                               html.Div(id='stocktwits-graphoutput',className='col s12 m6 l6'),
              #                                   ]),


            html.Div(id='graph-output', style={"height" : "50%", "width" : "90%",'margin-left':100}),
            #html.Div(id='stocktwits-graphoutput',  className='col s12 m6 l6',style={"height": "50%", "width": "50%"}),

            html.Div(children=[html.H1(children="Stock Twits Data",
                                       style={
                                           'textAlign': 'left',
                                           "background": "lightblue"})
                               ]
                     ),
            html.Div(children=[html.Table(id='stocktwits'),
                               html.Div(id='stocktwits-output', style={"height": "100%", "width": "100%","background": "lightblue"})])
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div(children=[html.Table(id='table'),
                               html.Div(id='table-output1',
                                        style={"height": "50%", "background": "lightblue", "width": "100%"})]),

            html.Div(children=[html.Table(id='table'),
                               html.Div(id='table-output',style={"height" : "50%","background": "lightblue", "width" : "100%"})])
        ])




def quick_color(s):
    # except return bg as app_colors['background']
    if s == 'positive':
        # positive
        return "#002C0D"
    elif s == 'negative':
        # negative:
        return "#270000"
    elif s == 'neutral':
        return 'grey'

app_colors = {
    'background': '#0C0F0A',
    'text': '#FFFFFF',
    'sentiment-plot':'#41EAD4',
    'volume-bar':'#FBFC74',
    'someothercolor':'#FFE4C4',
}








@app.callback(Output('stocktwits-output', 'children'),
              [Input('dropdown', 'value')])
def get_data_table2(option):
    df2 = getstocktwitsdata(option)
    df = df2[['created_at','body','sentiment']]
    #df = pd.DataFrame(df2)
    return html.Table(className="responsive-table",
                      children=[
                          html.Thead(
                              html.Tr(
                                  children=[
                                      html.Th(col.title()) for col in df.columns.values],
                                  style={'color': app_colors['text']}
                              )
                          ),
                          html.Tbody(
                              [

                                  html.Tr(
                                      children=[
                                          html.Td(data) for data in d
                                      ], style={'color': app_colors['text'],
                                                'background-color': quick_color(d[2])}
                                  )
                                  for d in df.values.tolist()])
                      ]
                      )

@app.callback(Output('table-output1', 'children'),
              [Input('dropdown', 'value')])
def get_data_table3(option):
    latestheadlines = yahoonewsheadlines(option)
    df2 = pd.DataFrame(latestheadlines,columns = ['headline','url'])
    df = df2[['headline']]
    data_table = dash_table.DataTable(

        id='datatable-data',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_table={'overflowY': 'auto','maxHeight' : 700 },
        style_header={'backgroundColor': 'rgb(0,250,154)'},
        style_cell={'font_size': '36px', 'backgroundColor': 'rgb(32,178,170)','textAlign': 'left','whiteSpace': 'normal',
            'height': 'auto'},
    )
    return data_table



@app.callback(Output('stocktwits-graphoutput', 'children'),
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





@app.callback(Output('graph-output', 'children'),
              [Input('date-input', 'start_date'),
               Input('date-input', 'end_date'),
               Input('dropdown', 'value')])
def render_graph(start_date, end_date, option):
    df = get_coin_data(crypto=option, start_date='2013-04-28', end_date='2020-04-28', save_data=None)
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
    #df2.columns = ['article.publish_date','article.title','url']
    #print('Index',df2)
    #df = pd.DataFrame(df2,columns = ['url','Headlines'])
    #print('Df Index',df)
    df = df2[['title','url']]
    dataframe = df
    rows = []
    for i in range(len(dataframe)):
        row = []
        for col in dataframe.columns:
            value = dataframe.iloc[i][col]
            # update this depending on which
            # columns you want to show links for
            # and what you want those links to be
            if col == 'url':
                cell = html.Td(html.A(href=value, children=value))
            else:
                cell = html.Td(children=value)
            row.append(cell)
        rows.append(html.Tr(row))
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns], style={'font-size': '200%','color': '#FFFFFF',
                                                                     'background-color': '#76e8a8'})] +

        rows,
        style={'color': 'blue',
               'background-color': 'lightyellow','font-size': '200%'}
    )




if __name__ == '__main__':
    app.run_server(debug=True)