import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

df_actors = pd.read_csv("./data/actors.tsv.gz", sep = "\t")                                                             
df_movies = pd.read_csv("./data/movies.tsv.gz", sep = "\t")
df_directors = pd.read_csv("./data/directors.tsv.gz", sep = "\t")

class movie:
    
    '''
    Initializes an object of the class 'movie'
    Takes a unique movie's identifier and includes class function to
    search for all actors in that movie recorded in the database.
    '''

    def __init__(self,identifier: str):
        self.id=identifier
    
    def search_actors(self,search_df):
        related_actors = search_df[search_df['knownForTitles'].apply(lambda x: self.id in x)]
        return related_actors.reset_index(drop=True)

class actor:
    
    '''
    Initializes an object of the class 'actor'
    Takes a unique actor's identifier and includes class function to 
    search for all movies that actor has recorded in the database.
    '''

    def __init__(self,identifier: str):
        self.id=identifier
    
    def search_movies(self,search_df):
        related_movies = search_df[search_df['nconst']==self.id]['knownForTitles']
        return related_movies.str.split(',').reset_index(drop=True)
    
def get_network(movie_titles, df_movies, df_actors):

    # Initialize movie objects
    movies = [movie(df_movies[df_movies['primaryTitle']==movie_title].iloc[0,0]) for movie_title in movie_titles]

    #searching for actors involved with the movie and making a list
    actors=[]
    for mv in movies:
        for identifier in mv.search_actors(df_actors)['nconst']:
            actors.append(identifier)
    actors = [actor(identifier) for identifier in np.unique(actors)]

    #searching for movies that those actors are involved with
    more_movies=[]
    for item in actors:
        more_movies+=item.search_movies(df_actors)[0]
    #reinitialize them as movie objects in a list 
    more_movies_objects=[movie(item) for item in np.unique(more_movies)]

    filtered_movies_df=df_movies[df_movies['tconst'].isin([mv.id for mv in more_movies_objects])]
    filtered_actors_df=df_actors[df_actors['nconst'].isin([actor.id for actor in actors])]

    #we can now repeat this process ad infinitum to expand the network of actors and movies.

    #use these dataframes to search for recommended movies with Marcine's algorithm
    return filtered_movies_df, filtered_actors_df

def recommend_movies(filtered_movies_df, filtered_actors_df, selected_genres, selected_actors, selected_directors, n=3):
    """
    Function to recommend movies based on user preferences.
    """
    # Initialize MultiLabelBinarizer
    mlb = MultiLabelBinarizer()

    #### GENRES ####
    # Convert genres to a list of genres
    filtered_movies_list = filtered_movies_df['genres'].apply(lambda x: x.split(','))

    # One-hot encode the genres
    genres_encoded = mlb.fit_transform(filtered_movies_list)
    selected_genres_encoded = mlb.transform([selected_genres])

    # Compute the cosine similarity matrix between the filtered movies and selected genres
    cosine_sims_genres = cosine_similarity(genres_encoded, selected_genres_encoded).flatten()
    

    ### ACTORS ###
    # Convert actors to a list of actors
    # for movie in filtered_movies_df: get identifier of movie, search for actors in filtered_actors_df
    # get the actors' names and append to a list
    if selected_actors:

        actors_list = []
        for idx, row in filtered_movies_df.iterrows():
            tconst = row['tconst']
            actors = filtered_actors_df[filtered_actors_df['knownForTitles'].apply(lambda x: tconst in x)]['primaryName']
            actors_list.append(actors.tolist())
        

        # One-hot encode the actors
        actors_encoded = mlb.fit_transform(actors_list)
        selected_actors_encoded = mlb.transform([selected_actors])

        # Compute the cosine similarity matrix between the filtered movies and selected actors
        cosine_sims_actors = cosine_similarity(actors_encoded, selected_actors_encoded).flatten()


    ### DIRECORS ###

    if selected_directors:
        directors_list = []
        for idx, row in filtered_movies_df.iterrows():
            tconst = row['tconst']
            directors = df_directors[df_directors['knownForTitles'].apply(lambda x: tconst in x)]['primaryName']
            # check directors for nan values and drop nan values
            directors = directors.dropna()
            if len(directors) == 0:
                continue
            directors_list.append(directors.tolist())
        
        
        
        # One-hot encode the directors
        directors_encoded = mlb.fit_transform(directors_list)
        selected_directors_encoded = mlb.transform([selected_directors])

        # Compute the cosine similarity matrix between the filtered movies and selected directors
        cosine_sims_directors = cosine_similarity(directors_encoded, selected_directors_encoded).flatten()




    # Combine the cosine similarities for genres and actors

    if not selected_actors and not selected_directors:
        cosine_sims = cosine_sims_genres
    elif not selected_directors:
        cosine_sims = 0.5 * cosine_sims_genres + 0.5 * cosine_sims_actors
    elif not selected_actors:
        cosine_sims = 0.5 * cosine_sims_genres + 0.5 * cosine_sims_directors
    else:
        cosine_sims = (1/3) * cosine_sims_genres + (1/3) * cosine_sims_actors + (1/3) * cosine_sims_directors





    # Get the indices of the most similar movies
    similar_movie_indices = np.argsort(cosine_sims)[::-1]
    
    # Select the top recommended movie
    recommended_movies = filtered_movies_df.iloc[similar_movie_indices[:n]]
    
    # # Print the recommended movie
    # print("Recommended Movie:", recommended_movie['primaryTitle'])
    return recommended_movies
    


### TESTING ###  -- comment out directors part in function if takes too long
# filtered_movies_df, filtered_actors_df  = get_network(['The Shawshank Redemption'], df_movies, df_actors)
# selected_genres = ['Adventure', 'Fantasy', 'Comedy']
# selected_actors = ['Tom Hanks', 'Morgan Freeman', 'Brad Pitt', 'Leonardo DiCaprio']
# selected_directors = ['Christopher Nolan', 'Steven Spielberg', 'Quentin Tarantino']
# recommend_movies(filtered_movies_df, filtered_actors_df, selected_genres=selected_genres, selected_actors=selected_actors, selected_directors=selected_directors)
