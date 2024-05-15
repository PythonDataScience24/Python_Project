import os
import pandas as pd
from Scripts.get_data import download_data
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL


# Get the required data and load them into dataframes
if not os.path.exists("./data") or not any(os.listdir("./data")):
    download_data()
df_actors = pd.read_csv("./data/actors.tsv.gz", sep = "\t")
df_movies = pd.read_csv("./data/movies.tsv.gz", sep = "\t")
df_directors = pd.read_csv("./data/directors.tsv.gz", sep = "\t")


app = Dash(__name__)

genres = ['Action', 'Drama', 'Horror', 'Comedy', 'Romance', 'Fantasy']

app.layout = html.Div([
    html.Div([
        html.Label('Input some movies you watched:'),
        html.Br(),
        dcc.Dropdown(id='movies-dropdown',
                     options=[],
                      multi=True, placeholder='Choose movies...'),
        html.Br(),
        html.Div(id='ratings-input-container'),
    ], style={'padding': 10, 'flex': 1}),

    html.Div([
        html.Label('Select your favorite genres:'),
        dcc.Dropdown(id='genres-dropdown', options=[{'label': genre, 'value': genre}
                                                    for genre in genres], multi=True),
        html.Br(),
        html.Label('Select your favorite actors:'),
        dcc.Dropdown(id='actors-dropdown', options=[], multi=True),
        html.Br(),
        html.Label('Select your favorite directors:'),
        dcc.Dropdown(id='directors-dropdown', options=[], multi=True),
    ], style={'padding': 10, 'flex': 1}),

    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-message', style={'padding': 10}),
], style={'display': 'flex', 'flexDirection': 'row'})

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
        return []
    return [html.Div([
        html.Label(f'Rating for {movie}:'),
        dcc.Input(id={'type': 'rating-input', 'index': movie}, type='number',
                  min=1, max=5, step=0.1)
    ]) for movie in selected_movies]

def search_term(search_value: str, df: pd.DataFrame, column: str) -> list:
    "Searches dataframe in specified column for term. Returns first ten results as list"
    search_results = df[df[column].str.contains(search_value, na = False, regex= False, case = False)][column].head(10).to_list()
    return search_results

@app.callback(
    Output('movies-dropdown', 'options'),
    Input('movies-dropdown', 'search_value'),
    State('movies-dropdown', 'value'), 
    prevent_initial_callback=True
)
def update_dropdown_options(search_value, selected_movies):
    """
    Updates dropdown options based on the search value.

    Args:
        search_value (str): The search value entered by the user.
        selected_movies (list): List of currently selected movies.

    Returns:
        list: List of dropdown options.
    """
    if not search_value:
        raise PreventUpdate
    current_values = selected_movies if selected_movies else []
    movie_titles =  search_term(search_value, df_movies, 'primaryTitle')
    movie_titles.extend(current_values) 
    return [{'label': title, 'value': title} for title in movie_titles] 

@app.callback(
    Output('actors-dropdown', 'options'),
    Input('actors-dropdown', 'search_value'),
    State('actors-dropdown', 'value'), prevent_initial_callback=True
)
def update_dropdown_options(search_value, selected_actors):
    """
    Updates dropdown options based on the search value.

    Args:
        search_value (str): The search value entered by the user.
        selected_actors (list): List of currently selected actors.

    Returns:
        list: List of dropdown options.
    """
    if not search_value:
        raise PreventUpdate 
    current_values = selected_actors if selected_actors else []
    actors =  search_term(search_value, df_actors, 'primaryName')
    actors.extend(current_values)
    return [{'label': title, 'value': title} for title in actors] 

@app.callback(
    Output('directors-dropdown', 'options'),
    Input('directors-dropdown', 'search_value'),
    State('directors-dropdown', 'value'), prevent_initial_callback=True
)
def update_dropdown_options(search_value, selected_directors):
    """
    Updates dropdown options based on the search value.

    Args:
        search_value (str): The search value entered by the user.
        selected_directors (list): List of currently selected directors.

    Returns:
        list: List of dropdown options.
    """
    if not search_value:
        raise PreventUpdate
    current_values = selected_directors if selected_directors else []
    directors =  search_term(search_value, df_directors, 'primaryName')
    directors.extend(current_values)
    return [{'label': title, 'value': title} for title in directors] 

@app.callback(
    Output('output-message', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('movies-dropdown', 'value'),
     State({'type': 'rating-input', 'index': ALL}, 'value'),
     State('actors-dropdown', 'value'),
     State('directors-dropdown', 'value'),
     State('genres-dropdown', 'value')]
)
def display_output(n_clicks, selected_movies, ratings, selected_actors, #pylint: disable=too-many-arguments
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
    if n_clicks > 0:
        if not selected_movies:
            return "Please select at least one movie."
        if not ratings:
            return "Please enter ratings for all selected movies."
        # Print selected options for testing
        print("Movies you watched:", selected_movies)
        print("\nRatings:", ratings)
        print("\nFavorite Genres:", selected_genres)
        print("\nFavorite Actors:", selected_actors)
        print("\nFavorite Directors:", selected_directors)
        # Return a confirmation message
        return html.Div([
            html.Label("You have selected:"),
            html.Br(),
            html.Label(f"\nMovies: {', '.join(selected_movies)}"),
            html.Br(),
            html.Label(f"\nRatings: {', '.join(str(rating) for rating in ratings)}"),
            html.Br(),
            html.Label(f"\nGenres: {', '.join(selected_genres) if selected_genres else 'None'}"),
            html.Br(),
            html.Label(f"\nActors: {', '.join(selected_actors) if selected_actors else 'None'}"),
            html.Br(),
            html.Label(f"\nDirectors: {', '.join(selected_directors) if selected_directors else 'None'}"),   #pylint: disable=line-too-long
            html.Br(),

        ])

    raise PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True)
