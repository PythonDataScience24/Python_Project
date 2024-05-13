import pandas as pd
import numpy as np
import networkx as nx

df_actors = pd.read_csv("./data/actors.tsv.gz", sep = "\t")                                                             
df_movies = pd.read_csv("./data/movies.tsv.gz", sep = "\t")
#df_directors = pd.read_csv("./data/directors.tsv.gz", sep = "\t")

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
    

#example input
movie_title='Everything Everywhere All at Once'
movie_data=df_movies[df_movies['primaryTitle']==movie_title]

#initializing the movie object
app_submission=movie(movie_data.iloc[0,1])
#searching for actors involved with the movie and making a list
actors=[]
for identifier in app_submission.search_actors(df_actors)['nconst']:
    actor_object=actor(identifier)
    actors.append(actor_object)

#searching for movies that those actors are involved with
more_movies=[]
for item in actors:
    more_movies+=item.search_movies(df_actors)[0]
#reinitialize them as movie objects in a list 
more_movies_objects=[movie(item) for item in np.unique(more_movies)]

filtered_movies_df=df_movies[df_movies['tconst'].isin(more_movies)]
original_titles=filtered_df['originalTitle'].tolist()
filtered_actors_df=df_actors[df_actors['nconst'].isin([actor.id for actor in actors])]

#we can now repeat this process ad infinitum to expand the network of actors and movies.

filtered_movies_df #use these dataframes to search for recommended movies with Marcine's algorithm
filtered_actors_df