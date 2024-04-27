from dash import Dash, dcc, html, Input, Output, State, callback

app = Dash(__name__)

app.layout = html.Div([
        html.Div(children=[

            html.Label('Select some movies!'),
            dcc.Dropdown(['list of data here','etc...'],multi=True),
            
            html.Br(),
            html.Label('Select some actors!'),
            dcc.Dropdown(['list of data here','Actors','etc...']
                ,multi=True),
        ], style={'padding': 10, 'flex': 1}),

        html.Div(children=[

            html.Label('Select some directors!'),
            dcc.Dropdown(['list of data here','etc...'],multi=True),

            html.Br(),
            html.Label('Select some studios!'),
            dcc.Dropdown(['list of data here','etc...'],multi=True),          ], style={'padding':10, 'flex':1}),
 
        html.Button('Submit',id='submit_val',n_clicks=0)
        ], style={'display': 'flex', 'flexDirection': 'row'})

if __name__ == '__main__':
    app.run(debug=True)
            
