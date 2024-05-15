import pandas as pd
import numpy as np
import networkx as nx

# df_actors = pd.read_csv("./data/actors.tsv.gz", sep = "\t")                                                             
# df_movies = pd.read_csv("./data/movies.tsv.gz", sep = "\t")
# df_directors = pd.read_csv("./data/directors.tsv.gz", sep = "\t")

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
    movies = [movie(df_movies[df_movies['primaryTitle']==movie_title].iloc[0,1]) for movie_title in movie_titles]

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
    return  filtered_movies_df, filtered_actors_df

def recommend_movies(preferences, df_movies, df_actors, df_directors):
    """
    Function to recommend movies based on user preferences.
    """
    # Filter movies based on genres, actors and directors
    genres = preferences[1]
    actors = preferences[2]
    directors = preferences[3]

    # Filter movies based on genres
    genre_movies = df_movies[df_movies['genres'].isin(genres)]

    # Filter movies based on actors
    preffered_actor_rows = df_actors[df_actors['primaryName'].isin(actors)]
    # get the movies from column knownForTitles and split them into a list
    preffered_movies = preffered_actor_rows['knownForTitles'].str.split(',').tolist()
    # get all movies from movies_df that are in the list of preffered_movies
    actor_movies = df_movies[df_movies['tconst'].isin([item for sublist in preffered_movies for item in sublist])]

    # Filter movies based on directors
    director_movies = df_directors[df_directors['primaryName'].isin(directors)]
    # get the movies from column knownForTitles and split them into a list
    director_movies = director_movies['knownForTitles'].str.split(',').tolist()
    # get all movies from df_movies that are in the list of director_movies
    director_movies = df_movies[df_movies['tconst'].isin([item for sublist in director_movies for item in sublist])]


    # Combine filtered movies
    recommended_movies = pd.concat([genre_movies, actor_movies, director_movies])

    # Remove duplicates
    recommended_movies = recommended_movies.drop_duplicates()

    # # Sort movies by rating
    # recommended_movies = recommended_movies.sort_values(by='rating', ascending=False)

    # preferred_movies is dict with movie names and ratings
    preferred_movies = preferences[0]
    # get the movies from movies_df that are in the preferred_movies
    # TODO or originalTitle?
    rated_movies = df_movies[df_movies['primaryTitle'].isin(preferred_movies.keys())]
    # add the ratings to the rated_movies
    rated_movies['rating'] = rated_movies['primaryTitle'].map(preferred_movies)



    ### Above part is good, below needs further work


"""
    # TODO split on knownForTitles and then merge with movies_df probably or implement by hand instead of using libs
    # Merge additional information (like actors and directors) into recommended_movies so that each movie has corresponding attributes that can be used for content-based filtering.
    recommended_movies = recommended_movies.merge(df_directors, on='knownForTitles', how='left')
    recommended_movies = recommended_movies.merge(df_actors, on='knownForTitles', how='left')

    # Convert genres to a list if it's a string of genres separated by commas
    recommended_movies['genres'] = recommended_movies['genres'].apply(lambda x: x.split(','))

    # One-hot encode genres
    mlb = MultiLabelBinarizer()
    genres_encoded = mlb.fit_transform(recommended_movies['genres'])

    # Add new features back to df_B
    recommended_movies = recommended_movies.join(pd.DataFrame(genres_encoded, columns=mlb.classes_, index=recommended_movies.index))

    # Calculate similarity between all movies
    similarity_matrix = cosine_similarity(genres_encoded)

    # Only consider movies you've rated
    rated_indices = rated_movies['tconst'].isin(recommended_movies['tconst'])
    weighted_scores = similarity_matrix[rated_indices].T.dot(rated_movies['rating'])





    # Return top 5 movies
    return recommended_movies.head(5)

user_preferences = input_preferences()
recommend_movies(user_preferences)
"""