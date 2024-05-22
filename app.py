import os
import pandas as pd
from Scripts.get_data import download_data
from Scripts.movie_recommendation_v2 import get_network, recommend_movies
from dash import Dash, dcc, html, Input, Output, State, dash_table
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
import dash_bootstrap_components as dbc
import plotly.express as px  # Import plotly.express for visualization
import plotly.graph_objects as go  # Import plotly.graph_objects for pie chart

# Get the required data and load them into dataframes
if not os.path.exists("./data") or not any(os.listdir("./data")):
    download_data()
df_actors = pd.read_csv("./data/actors.tsv.gz", sep="\t")
df_movies = pd.read_csv("./data/movies.tsv.gz", sep="\t")
df_directors = pd.read_csv("./data/directors.tsv.gz", sep="\t")

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

genres = ['Action', 'Drama', 'Horror', 'Comedy', 'Romance', 'Fantasy', 'Sci-Fi', 'Crime', 'Sport', 'Mystery', 'Adventure', 'Thriller', 'Biography']

MOVIES = [
    dbc.CardHeader(html.H4("My movies")),
    dbc.CardBody([
        html.Div([
            dbc.Button("Add", id='add-movies-button', color='info', outline=True, size='sm', n_clicks=0),
        ], className='d-grid gap-2 d-md-flex justify-content-md-center'),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Input some movies you watched:'), close_button=True),
            dbc.ModalBody([
                dcc.Dropdown(id='movies-dropdown', multi=True, placeholder='Choose movies...'),
                html.Br(),
                html.Div(id='ratings-input-container'),
                html.Br(),
                dbc.Button('Submit', id='movie-submission-button', n_clicks=0)
            ])
        ], id='movie-modal', scrollable=True),
        html.Div(id='movie-output-message'),
    ])
]

OTHER = [
    dbc.CardHeader(html.H4('My Genres, Directors and Actors')),
    dbc.CardBody([
        html.Div([
            dbc.Button("Add", id='add-other-button', color='info', outline=True, size='sm', n_clicks=0),
        ], className='d-grid gap-2 d-md-flex justify-content-md-center'),
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle('Input Genres, Actors or Directors'), close_button=True),
            dbc.ModalBody([
                html.Label('Select your favorite genres:'),
                dcc.Dropdown(id='genres-dropdown', options=[{'label' : genre, 'value' : genre} for genre in genres], multi=True),
                html.Br(),
                html.Label('Select your favorite actors:'),
                dcc.Dropdown(id='actors-dropdown', options=[], multi=True),
                html.Br(),
                html.Label('Select your favorite directors:'),
                dcc.Dropdown(id='directors-dropdown', options=[], multi=True),
                html.Br(),
                dbc.Button('Submit', id='other-submission-button', n_clicks=0)
            ], style={'padding': 10, 'flex': 1}),
        ], id='other-modal'),
        html.Div(id='other-output-message'),
    ])
]

app.layout = html.Div([
    dcc.Store(id = 'movie-store', storage_type = 'memory'),
    dcc.Store(id = 'other-store', storage_type = 'memory'),
    dbc.Container([
        dbc.Row([
            dbc.Col(dbc.Card(MOVIES, outline=True)),
            dbc.Col(dbc.Card(OTHER, outline=True))
        ]),
        dbc.Row([
            dbc.Button('Get Movie Recommendations', id='submit-button'),
        ], style = {'marginTop' : 40}, className="d-grid gap-2  col-6 mx-auto"),
        dcc.Loading(
            children = [
                dbc.Row([
                    html.Div(id='output-message', style={'padding': 10}),
                ], style={'marginTop': 40}),],
            id = "loading",
            type="default"),
    ], style={'marginTop': 40})
])


@app.callback(
    Output('ratings-input-container', 'children'),
    [Input('movies-dropdown', 'value')]
)
def update_ratings_input(selected_movies):
    """
    Updates the ratings input based on selected movies.

    Args:
        selected_movies (list): List of selected movies.

    Returns:
        list: List of HTML div elements containing rating inputs.
    """
    if not selected_movies:
        raise PreventUpdate
    return [
        dbc.Row([
            dbc.Col(html.Label(f'Rating for {movie}:'), width=4),
            dbc.Col(
                dcc.Slider(
                    1, 10, 1,
                    id={'type': 'rating-input', 'index': movie},
                    value=5
                )
            )
        ], className="mb-2")
        for movie in selected_movies
    ]

def search_term(search_value: str, df: pd.DataFrame, column: str) -> list:
    "Searches dataframe in specified column for term. Returns first ten results as list"
    search_results = df[df[column] == search_value][column].to_list()
    return search_results

def update_dropdown_options(search_value, selected_items, df, column_name):
    """
    Updates dropdown options based on the search value.

    Args:
        search_value (str): The search value entered by the user.
        selected_items (list): List of currently selected items.
        df (DataFrame): DataFrame to search in.
        column_name (str): Column name to search in the DataFrame.

    Returns:
        list: List of dropdown options.
    """
    if not search_value:
        raise PreventUpdate
    
    current_values = selected_items if selected_items else []
    items = search_term(search_value, df, column_name)
    items.extend(current_values)
    return [{'label': item, 'value': item} for item in items]

@app.callback(
    Output('movies-dropdown', 'options'),
    Input('movies-dropdown', 'search_value'),
    State('movies-dropdown', 'value'),
    prevent_initial_callback=True
)
def update_movies_dropdown_options(search_value, selected_movies):
    return update_dropdown_options(search_value, selected_movies, df_movies, 'primaryTitle')

@app.callback(
    Output('actors-dropdown', 'options'),
    Input('actors-dropdown', 'search_value'),
    State('actors-dropdown', 'value'),
    prevent_initial_callback=True
)
def update_actors_dropdown_options(search_value, selected_actors):
    return update_dropdown_options(search_value, selected_actors, df_actors, 'primaryName')

@app.callback(
    Output('directors-dropdown', 'options'),
    Input('directors-dropdown', 'search_value'),
    State('directors-dropdown', 'value'),
    prevent_initial_callback=True
)
def update_directors_dropdown_options(search_value, selected_directors):
    return update_dropdown_options(search_value, selected_directors, df_directors, 'primaryName')

@app.callback(
    Output('output-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('movies-dropdown', 'value'),
     State({'type': 'rating-input', 'index': ALL}, 'value'),
     State('actors-dropdown', 'value'),
     State('directors-dropdown', 'value'),
     State('genres-dropdown', 'value')],
)
def display_output(n_clicks, selected_movies, ratings, selected_actors,  # pylint: disable=too-many-arguments
                   selected_directors, selected_genres):
    """
    Displays the selected movie information.

    Args:
        n_clicks (int): Number of button clicks.
        selected_movies (list): List of selected movies.
        ratings (list): List of movie ratings.
        selected_actors (list): List of selected actors.
        selected_directors (list): List of selected directors.
        selected_genres (list): List of selected genres.

    Returns:
        list: List of HTML elements representing selected movie information.
    """
    if n_clicks:
        if not selected_movies:
            return "Please select at least one movie."
        if not ratings:
            return "Please enter ratings for all selected movies."
        filtered_df, filtered_actors_df = get_network(selected_movies, df_movies, df_actors)
        recommended_movies = recommend_movies(filtered_df, filtered_actors_df, selected_genres, selected_actors, selected_directors, n=10)
        # filtered_df = filtered_df.head(10)
        # return dash_table.DataTable(filtered_df.to_dict('records'), [{"name": i, "id": i} for i in filtered_df.columns])
        
        # Creating a bar chart using plotly express
        fig_bar = px.bar(
            recommended_movies,
            x='primaryTitle',
            y=recommended_movies.index,  # Using index as y value
            labels={'primaryTitle': 'Movie Title', 'index': 'Recommendation Rank'},
            title='Recommended Movies'
        )
        
        # Prepare data for pie chart
        genres_list = recommended_movies['genres'].str.split(',').explode()
        genre_counts = genres_list.value_counts().reset_index()
        genre_counts.columns = ['Genre', 'Count']
        
        # Creating a pie chart using plotly.graph_objects
        fig_pie = go.Figure(data=[go.Pie(labels=genre_counts['Genre'], values=genre_counts['Count'], hole=.3)])
        fig_pie.update_layout(title_text='Genre Distribution of Recommended Movies')
        
        return html.Div([
            dcc.Graph(figure=fig_bar),
            dcc.Graph(figure=fig_pie)
        ])
    raise PreventUpdate

def toggle_modal(n1, n2, is_open):
    """Toggles modal elements with open and close buttons"""
    if n1 or n2:
        return not is_open
    return is_open

app.callback(
    Output("movie-modal", "is_open"),
    [Input("add-movies-button", "n_clicks"),
     Input("movie-submission-button", "n_clicks")],
    State("movie-modal", "is_open"),
)(toggle_modal)

app.callback(
    Output("other-modal", "is_open"),
    [Input("add-other-button", "n_clicks"),
    Input("other-submission-button", "n_clicks")],
    State("other-modal", "is_open"),
)(toggle_modal)

@app.callback(
    Output('movie-store', 'data'),
    [Input('movie-submission-button', 'n_clicks')],
    [State('movies-dropdown', 'value'),
     State({'type': 'rating-input', 'index': ALL}, 'value')]
)
def save_movie_inputs(n_clicks, selected_movies, ratings):
    """
    Saves selected movies and ratings into a dcc.Store element 

    Args:
        n_clicks (int): Number of button clicks.
        selected_movies (list): List of selected movies.
        ratings (list): List of ratings.

    Returns:
        dict: Dictionary containing saved inputs.
    """
    if not n_clicks or not selected_movies:
        raise PreventUpdate
    else:
        return {'movies': selected_movies, 'ratings': ratings}

@app.callback(
    Output('movie-output-message', 'children'),
    [Input('movie-store', 'data')]
)
def display_movie_output(data):
    """
    Displays information for selected movies and ratings 

    Args:
        data (dict): Dictionary containing saved inputs.

    Returns:
        list: List of HTML elements representing selected information.
    """
    if not data:
        raise PreventUpdate
    else:
        selected_movies = data.get('movies', [])
        ratings = data.get('ratings', [])
        data = [{'Title': movie, 'Rating': rating} for movie, rating in zip(selected_movies, ratings)]
        table = dash_table.DataTable(
            id='movie-table',
            columns=[{'name': col, 'id': col} for col in ['Title', 'Rating']],
            data=data,
            style_table={'overflowX': 'scroll'},
        )
        return table

@app.callback(
    Output('other-store', 'data'),
    [Input('other-submission-button', 'n_clicks')],
    [State('actors-dropdown', 'value'),
     State('directors-dropdown', 'value'),
     State('genres-dropdown', 'value')]
)
def save_other_inputs(n_clicks, selected_actors, selected_directors, selected_genres):
    """
    Saves selected actors, directors, and genres into a dcc.Store element 

    Args:
        n_clicks (int): Number of button clicks.
        selected_actors (list): List of selected actors.
        selected_directors (list): List of selected directors.
        selected_genres (list): List of selected genres.

    Returns:
        dict: Dictionary containing saved inputs.
    """
    if not n_clicks or not (selected_directors or selected_actors or selected_genres):
        raise PreventUpdate
    else:
        return {'actors': selected_actors, 'directors': selected_directors, 'genres': selected_genres}

@app.callback(
    Output('other-output-message', 'children'),
    [Input('other-store', 'data')]
)
def display_other_output(data):
    """
    Displays information for selected actors, directors, and genres 

    Args:
        data (dict): Dictionary containing saved inputs.

    Returns:
        list: List of HTML elements representing selected information.
    """
    if not data:
        raise PreventUpdate
    else:
        selected_actors = data.get('actors', [])
        selected_directors = data.get('directors', [])
        selected_genres = data.get('genres', [])
        data = [{'Genres': ', '.join(selected_genres) if selected_genres else 'None',
                 'Actors': ', '.join(selected_actors) if selected_actors else 'None',
                 'Directors': ', '.join(selected_directors) if selected_directors else 'None'}]
        table = dash_table.DataTable(
            id='other-table',
            columns=[{'name': col, 'id': col} for col in ['Genres', 'Actors', 'Directors']],
            data=data,
            style_table={'overflowX': 'scroll'},
        )
        return table

if __name__ == '__main__':
    app.run_server(debug=True)

