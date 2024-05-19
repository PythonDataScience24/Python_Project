import os
import requests
import pandas as pd
from typing import List, Tuple

def download_file(url: str, save_path : str):
    """Downloads file from url locally to the specified path """

    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
    except requests.RequestException as e:
        print(f"Error downloading {url}: {e}")
    except OSError as e:
        print(f"Error saving {save_path}: {e}")

def filter_by_term(df: pd.DataFrame, col: str, terms: Tuple[str, ...] | List[str]) -> pd.DataFrame:
    """Returns a new DataFrame containing only rows where col contains the desired terms"""

    terms = '|'.join(terms)
    return df[df[col].str.contains(terms, case = False, na= False)]

def download_data():

    URL_NAME = "https://datasets.imdbws.com/name.basics.tsv.gz"
    PATH_NAME = "./data/name.basics.tsv.gz"
    URL_TITLE = "https://datasets.imdbws.com/title.basics.tsv.gz"
    PATH_TITLE = "./data/title.basics.tsv.gz"

    PATH_DIRECTORS = "./data/directors.tsv.gz"
    PATH_MOVIES = "./data/movies.tsv.gz"
    PATH_ACTORS = "./data/actors.tsv.gz"

    download_file(URL_NAME, PATH_NAME)
    download_file(URL_TITLE, PATH_TITLE)
    df_name = pd.read_csv(PATH_NAME, sep = "\t", usecols=lambda x: x not in ['birthYear', 'deathYear'])
    df_title = pd.read_csv(PATH_TITLE, sep = "\t", usecols=lambda x: x not in ['runtimeMinutes', 'startYear', 'endYear', 'isAdult'])

    # Filter by actors and directors, filter out titles that are not movies
    df_actors = filter_by_term(df_name, 'primaryProfession', ['actor', 'actress'])
    df_directors = filter_by_term(df_name, 'primaryProfession', ['director'])
    df_movies = filter_by_term(df_title, 'titleType', ['movie', 'short', 'tvMovie'])
    
    df_movies.to_csv(PATH_MOVIES, sep = '\t', compression='gzip', index=False)
    df_actors.to_csv(PATH_ACTORS, sep = '\t', compression='gzip', index=False)
    df_directors.to_csv(PATH_DIRECTORS, sep = '\t', compression='gzip', index=False)

    os.remove(PATH_NAME)
    os.remove(PATH_TITLE)

if __name__ == "__main__":
    download_data()