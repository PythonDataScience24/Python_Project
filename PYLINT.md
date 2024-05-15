# PYLINT
The highlighted lines (**) on the PYLINT output are the ones we corrected. The lines where it's corrected are also highlighted in the code (lines with 💡).

## PYLINT output on app.py
```plaintext
************* Module app
**app.py:50:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:57:0: C0301: Line too long (102/100) (line-too-long)**

**app.py:65:0: C0301: Line too long (119/100) (line-too-long)**

**app.py:68:0: C0301: Line too long (143/100) (line-too-long)**

**app.py:71:0: C0301: Line too long (162/100) (line-too-long)**

**app.py:96:0: C0301: Line too long (101/100) (line-too-long)**

**app.py:117:9: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:122:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:123:71: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:135:0: C0301: Line too long (109/100) (line-too-long)**

**app.py:153:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:156:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:163:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:164:0: C0303: Trailing whitespace (trailing-whitespace)**

**app.py:177:0: C0301: Line too long (106/100) (line-too-long)**

**app.py:186:0: C0303: Trailing whitespace (trailing-whitespace)**

app.py:1:0: C0114: Missing module docstring (missing-module-docstring)

app.py:12:4: W1510: 'subprocess.run' used without explicitly defining the value for 'check'. (subprocess-run-check)

app.py:34:12: C0209: Formatting a regular string which could be a f-string (consider-using-f-string)

**app.py:115:4: R1720: Unnecessary "else" after "raise", remove the "else" and de-indent the code inside it (no-else-raise)**

**app.py:135:0: R0913: Too many arguments (6/5) (too-many-arguments)**

-----------------------------------
Your code has been rated at 5.62/10
```

## code after fixing the issues
```plaintext
import os
import subprocess
import pandas as pd
from dash import Dash, dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import ALL
from SPARQLWrapper import SPARQLWrapper, JSON


# Get the required data and load them into dataframes
if not os.path.exists("./data") or not any(os.listdir("./data")):
    subprocess.run(["python3", "./Scripts/get_data.py"])
df_actors = pd.read_csv("./data/actors.tsv.gz", sep = "\t")
df_movies = pd.read_csv("./data/movies.tsv.gz", sep = "\t")
#df_directors = pd.read_csv("./data/directors.tsv.gz", sep = "\t")


app = Dash(__name__)


genres = ['Action', 'Drama', 'Horror', 'Comedy', 'Romance', 'Fantasy']

def query_sparql(search_value):
    """
    Queries Wikidata to search for movies based on the given search value.

    Args:
        search_value (str): The value to search for in Wikidata.

    Returns:
        dict: JSON response containing search results.
    """
    sparql = SPARQLWrapper('https://query.wikidata.org/sparql')
    query = """
    SELECT DISTINCT ?item ?itemLabel ?itemDescription WHERE {
        ?item ?label "%s"@en.
        ?item (wdt:P31/wdt:P279*) wd:Q11424.  # Ensure the item is an instance of a film
        ?article schema:about ?item.
        ?article schema:inLanguage "en".
        ?article schema:isPartOf <https://en.wikipedia.org/>.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """ % search_value

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return results


app.layout = html.Div([
    html.Div([
        html.Label('Input some movies you watched:'),
        html.Br(),
        dcc.Dropdown(id='movies-dropdown',
                     options=[{'label' : i, 'value' : i}
                              for i in df_movies['primaryTitle'].head(10)],
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
        dcc.Dropdown(id='actors-dropdown', options=[{'label': name, 'value': name}
                        for name in df_actors['primaryName'].head(10)], multi=True),
        html.Br(),
        html.Label('Select your favorite directors:'),
        #dcc.Dropdown(id='directors-dropdown', options=[{'label': director, 'value': director}
        #for director in df_directors['primaryName'].head(10)], multi=True),
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

@app.callback(
    Output('movies-dropdown', 'options'),
    Input('movies-dropdown', 'search_value'),
    State('movies-dropdown', 'value')
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
    results = query_sparql(search_value)
    movie_titles = [result['itemLabel']['value'] for result in results['results']['bindings']]
    movie_titles.extend(current_values)
    return [{'label': title, 'value': title} for title in movie_titles]


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
```
## PYLINT output after fixing the issus in app.py
```plaintext
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)

app.py:12:4: W1510: 'subprocess.run' used without explicitly defining the value for 'check'. (subprocess-run-check)

app.py:34:12: C0209: Formatting a regular string which could be a f-string (consider-using-f-string)

------------------------------------------------------------------
Your code has been rated at 9.38/10 (previous run: 9.17/10, +0.21)
```