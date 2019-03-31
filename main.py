import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output,State
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

df1 = pd.read_csv("YieldCurve.csv").set_index('DATE')
df2 = pd.read_csv("SPX.csv").set_index('DATE')
global i
i = 0

app.layout = html.Div([
    # Header
    html.Div([
        html.H2(
            'Inverted Yield Curve Overview',
            style={'float': 'center',}
        ),   
    ]),

    # All-Items
    html.Div([
        # Select Time Period
        html.Div([
            html.Label('Select Time Period:'),
            dcc.Dropdown(
                id = 'period',
                options=[
                    {'label': 'Year 1989', 'value': 't1'},
                    {'label': 'Year 2000', 'value': 't2'},
                    {'label': 'Year 2006', 'value': 't3'},
                    {'label': 'Year 2019', 'value': 't4'},
                ],
                value='t4',
                style={'width':'60%'},
            ),
        ],style={'marginBottom':10, 'marginTop':10}),
        # Display Module
        html.Div([
            html.Label('Display Module:'),
            dcc.Dropdown(
                id='is_plot',
                options=[
                    {'label': 'Treasury Yield Curve', 'value': 'YC'},
                    {'label': 'SPX Index', 'value': 'SPX'}
                ],
                value=['YC', 'SPX'],
                multi=True,
                style={'width':'60%'},
            ),            
        ],style={'marginBottom':10, 'marginTop':10}),
        # Display Mode
        html.Div([
            html.Label('Display Mode:'),
            dcc.RadioItems(
                id='mode',
                options=[
                    {'label': 'Auto', 'value': 'auto'},
                    {'label': 'Manual', 'value': 'man'},
                ],
                value='auto',
                labelStyle={'display': 'inline-block'}
            )
        ],style={'marginBottom':10, 'marginTop':10}),
        # Time Range
        html.Div([
            html.Label('Timing:'),
            html.Div(id='timing'),
        ],style={'marginBottom':10, 'marginTop':10}),
        html.Div([
            dcc.Slider(
                id='range',
                min=0,
                max=len(df1)-1,
                value=0,
                marks={i:str(df1.index[i]) for i in range(0,len(df1),10)},
                updatemode='drag',
            ),
        ],style={'marginBottom':50, 'marginTop':10, 'marginLeft':50, 'marginRight':50}),
        # Interval
        html.Div([
            dcc.Interval(
                id='interval',
                interval=800,
                n_intervals=0
            )
        ]),
        # Hidden Div for slice_df1, slice_df2
        html.Div(id='hid1', style={'display':'none'})
    ]),

    # Two Graphs
    html.Div([
        html.Div([
            dcc.Graph(
                id = 'yc_graph',
            ),
        ], className='six columns'),

        html.Div([
            dcc.Graph(
                id = 'spx_graph',
            )
        ], className='six columns'),
    ],className='row'),

])

def plot_yc(filtered_df1, input_is_plot):
    if 'YC' in input_is_plot:
        return {
            'data': [go.Scatter(
                x = filtered_df1.columns,
                y = filtered_df1.values[0],
                mode = 'lines',
            )],
            'layout': go.Layout(
                title='Treasury Yield Curve',
                xaxis={'title': 'Maturity'},
                yaxis={'title': 'Interest Rate'},
                margin={'l': 50, 'b': 40, 't': 100, 'r': 50},
                legend={'x': 0, 'y': 1},
                hovermode='closest'
            )
        }
    else:
        return {'data': [{'x':None, 'y':None}]}

def plot_spx(filtered_df2, input_is_plot):
    if 'SPX' in input_is_plot:
        return {
            'data': [go.Scatter(
                x = filtered_df2.index,
                y = filtered_df2['Close'].values,
                mode = 'lines',
            )],
            'layout': go.Layout(
                title='SPX Index',
                xaxis={'title': 'Time'},
                yaxis={'title': 'Price'},
                margin={'l': 50, 'b': 40, 't': 100, 'r': 50},
                hovermode='closest'
            ),}
    else:
        return {'data': [{'x':None, 'y':None}]}

# autoplay1
@app.callback(
    [Output('range', 'disabled'), 
    Output('range', 'value'),],
    [Input('mode', 'value'), 
    Input('interval', 'n_intervals')],
    [State('range','value')])
def autoplay(input_mode, n, state_range):
    if input_mode == 'auto':
        if n == 0:
            with open('i.txt', 'w') as f:
                f.write('0')
        else:
            with open('i.txt', 'r') as f:
                i = int(f.read())
            i += 1
            with open('i.txt', 'w') as f:
                f.write(str(i))
            return True, i
    else:
        with open('i.txt', 'w') as f:
            f.write(str(state_range))
        return False, state_range


# update period -> time range
@app.callback(
    [Output('range','max'),Output('range', 'marks'),Output('hid1', 'children')],
    [Input('period', 'value')])
def update_time_range(input_period):

    if input_period == 't1':
        startpoint = '1989-01-01'
        endpoint = '1990-10-18'
    elif input_period == 't2':
        startpoint = '2000-01-01'
        endpoint = '2002-10-31'        
    elif input_period == 't3':
        startpoint = '2006-06-01'
        endpoint = '2009-03-01'
    else:
        startpoint = '2018-12-01'
        endpoint = '2019-03-27'
    slice_df1 = df1[(df1.index >= startpoint) & (df1.index <= endpoint)]
    slice_df2 = df2[(df2.index >= startpoint) & (df2.index <= endpoint)]
    slice_df1.to_csv('slice_df1.csv')
    slice_df2.to_csv('slice_df2.csv')

    if input_period in ['t1','t2','t3']:
        return (
            len(slice_df1)-1, 
            {i: str(slice_df1.index[i]) for i in range(0,len(slice_df1),21)},
            True,
        )
    else:
        return (
            len(slice_df1)-1, 
            {i: str(slice_df1.index[i]) for i in range(0,len(slice_df1),5)},
            True,
        )        


# update time range -> timing
@app.callback(
    Output('timing', 'children'),
    [Input('range', 'value')])
def update_timing(input_range):
    return pd.read_csv('slice_df1.csv').set_index('DATE').index[input_range]

# # update graph YieldCurve
@app.callback(
    Output('yc_graph', 'figure'),
    [Input('is_plot', 'value'),
    Input('range', 'value'),])
def update_graph1(input_is_plot, input_range):
    filtered_df1 = pd.read_csv('slice_df1.csv').set_index('DATE')
    filtered_df1 = filtered_df1[filtered_df1.index == filtered_df1.index[input_range]]
    return plot_yc(filtered_df1, input_is_plot)


# # # update graph SPXIndex
@app.callback(
    Output('spx_graph', 'figure'),
    [Input('is_plot', 'value'),
    Input('range', 'value'),])
def update_graph2(input_is_plot, input_range):
    filtered_df2 = pd.read_csv('slice_df2.csv').set_index('DATE')[:input_range]
    return plot_spx(filtered_df2, input_is_plot)

if __name__ == '__main__':
    app.run_server(debug=True)
