import dash
import dash_core_components as dcc
import dash_html_components as html
# import pandas as pd

app = dash.Dash()

app.layout = html.Div(children=[
    dcc.Input(id='input', value='Enter something', type='text'),
    html.Div(id='output')
    ])

@app.callback(
    dash.dependencies.Output(component_id='output', component_property='children'),
    [dash.dependencies.Input(component_id='input', component_property='value')])
def update_value(input_data):
    try:
        return str(float(input_data)**2)
    except:
        return "Some error"
# if __name__ == '__main__':
#     app.run_server()
    # pd.read_csv("SPX.csv")
    # pd.read_csv("YieldCurve.csv")
