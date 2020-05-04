from app import app
from app import server
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from datetime import datetime
import dash_table
import pandas as pd
from data import yahoonewsdata,get_coin_data,getstocktwitsdata

colors = {
    'background': '#000000',
    'background2': '#FF0',
    'text': 'yellow'
    }
coin_list = ['AMZN','WMT','COST','KR']


app.layout = html.Div([html.H1('Retail Innovation Center Stock Analysis Dashboard',
                               style={
                                      'textAlign': 'center',
                                      "background": "yellow"}),
               html.Div(['Select Dates',
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
                          'font-size': '18px',
                          'margin': 0,
                          'padding': '8px',
                          'background': 'yellow',
                   }
               ),
               '-|- Select Ticker here',
               dcc.Dropdown(id='dropdown',
                            options=[{'label': i, 'value': i} for i in coin_list],
                            value='AMZN',
                            optionHeight=20,
                            style={
                                'height': '50px',
                                'font-weight': 100,
                                'font-size': '16px',
                                'line-height': '10px',
                                'color': 'gray',
                                'margin': 0,
                                'padding': '8px',
                                'background': 'yellow',
                                'position': 'middle',
                                'display': 'inline-block',
                                'width': '150px',
                                'vertical-align': 'middle',
                                }
                            ),
                html.Div(id='date-output'),
                html.Div(id='intermediate-value', style={'display': 'none'}),
                               ], className="row ",
                    style={'marginTop': 0, 'marginBottom': 0, 'font-size': 30, 'color': 'white',
                           'display': 'inline-block'}),

                html.Div([
                dcc.Tabs(id='tabs-example', value='tab-1', children=[
                    dcc.Tab(label='Stock Price', value='tab-1'),
                    dcc.Tab(label='Stock News -Ticker', value='tab-2'),
                ]),
                html.Div(id='tabs-example-content')
                ]),


               html.Div(children=[dcc.Markdown(" Retail Tech")], style={'textAlign': 'center',"background": "yellow"}),
                              ],
              style={"background": "#000080"}
                            )

@app.callback(Output('tabs-example-content', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.Div(id='graph-output', style={"height" : "50%", "width" : "50%"}),
            html.Div(children=[html.H1(children="Stock Twits Data",
                                       style={
                                           'textAlign': 'left',
                                           "background": "yellow"})
                               ]
                     ),
            html.Div(children=[html.Table(id='stocktwits'),
                               html.Div(id='stocktwits-output', style={"height": "100%", "width": "100%"})])
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.Div(children=[html.Table(id='table'), html.Div(id='table-output',style={"height" : "100%", "width" : "100%"})])
        ])


@app.callback(Output('table-output', 'children'),
              [Input('dropdown', 'value')])
def get_data_table(option):
    latestheadlines = yahoonewsdata(option)
    df2 = pd.DataFrame(latestheadlines,columns = ['headline','url'])
    df = df2[['headline']]
    data_table = dash_table.DataTable(

        id='datatable-data',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_table={'overflowY': 'auto','maxHeight' : 700 },
        style_header={'backgroundColor': 'rgb(0,250,154)'},
        style_cell={'font_size': '26px', 'backgroundColor': 'rgb(32,178,170)','textAlign': 'left','whiteSpace': 'normal',
            'height': 'auto'},
    )
    return data_table


@app.callback(Output('stocktwits-output', 'children'),
              [Input('dropdown', 'value')])
def get_data_table(option):
    df2 = getstocktwitsdata(option)
    df = df2[['created_at','body']]
    #df = pd.DataFrame(df2)
    data_table = dash_table.DataTable(

        id='datatable-data',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        style_table={'overflowY': 'auto','maxHeight' : 700 },
        style_header={'backgroundColor': 'rgb(0,250,154)'},
        style_cell={'font_size': '26px', 'backgroundColor': 'rgb(32,178,170)','textAlign': 'left','whiteSpace': 'normal',
            'height': 'auto'},
    )
    return data_table




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


if __name__ == '__main__':
    app.run_server(debug=True)