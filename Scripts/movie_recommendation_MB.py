import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

# Task 1:
# Allow users to input their favorite movie along with their ratings. Users can
# also input their favorite movie genres, actors and directors to cusztomize their preferences.

def input_preferences():
    # Input movie name
    movies = {}
    # TODO If input is already in the dictionary/list, don't add (only if rating differs?)
    while True:
        try:
            movie_name = input("Enter your favorite movies. To exit, type 'exit'. \n Enter movie name: ")
            if movie_name == "":
                raise ValueError
        except ValueError:
            print("Please enter a valid movie name. \n")
        if movie_name == "exit":
                break
        else:
            try:
                movie_rating = int(input("Enter your rating for the movie in range 1-5. \n Enter rating: "))
                if type(movie_rating) != int or movie_rating < 1 or movie_rating > 5:
                    raise ValueError
                else: 
                    movies[movie_name] = movie_rating
            except ValueError:
                print("Please enter a valid movie rating. Rating should be an integer between 1 and 5. \n")
            
    genres = []
    while True:
        try:
            movie_genre = input("Enter your favorite movie genres. To exit, type 'exit'. \n Enter movie genre: ")
            if movie_genre == "":
                raise ValueError
        except ValueError:
            print("Please enter a valid movie genre. ")
        if movie_genre == "exit":
                break
        else:
            genres.append(movie_genre)
             
    actors = []
    while True:
        try:
            movie_actor = input("Enter your favorite movie actors. To exit, type 'exit'. \n Enter movie actor: ")
            if movie_actor == "":
                raise ValueError
        except ValueError:
            print("Please enter a valid movie actor. \n")
        if movie_actor == "exit":
                break
        else:
            actors.append(movie_actor)
    
    directors = []
    while True:
        try:
            movie_director = input("Enter your favorite movie directors. To exit, type 'exit'. \n Enter movie director: ")
            if movie_director == "":
                raise ValueError
        except ValueError:
            print("Please enter a valid movie director. \n")
        if movie_director == "exit":
                break
        else:
            directors.append(movie_director)

    return movies, genres, actors, directors


dataPath = '/Users/marcinebessire/Library/Mobile Documents/com~apple~CloudDocs/Documents/Master UniBe/2nd semester 2024/Advanced Python/Project/data/directors.tsv'

movies_df = pd.read_csv(dataPath + '/movies.tsv', sep='\t')
# drop colunn Unnamed: 0
movies_df = movies_df.drop(columns=['Unnamed: 0'])

actors_df = pd.read_csv(dataPath + '/actors.tsv', sep='\t')
directors_df = pd.read_csv(dataPath + '/directors.tsv', sep='\t')



# Task 2:
# Develop a basic recommendation algorithm that suggests new movies based on the user's preferences and ratings. Retrieve and display the top 5 movie recommendations.

def recommend_movies(preferences):
    """
    Function to recommend movies based on user preferences.
    """
    # Filter movies based on genres, actors and directors
    genres = preferences[1]
    actors = preferences[2]
    directors = preferences[3]

    # Filter movies based on genres
    genre_movies = movies_df[movies_df['genres'].isin(genres)]

    # Filter movies based on actors
    preffered_actor_rows = actors_df[actors_df['primaryName'].isin(actors)]
    # get the movies from column knownForTitles and split them into a list
    preffered_movies = preffered_actor_rows['knownForTitles'].str.split(',').tolist()
    # get all movies from movies_df that are in the list of preffered_movies
    actor_movies = movies_df[movies_df['tconst'].isin([item for sublist in preffered_movies for item in sublist])]

    # Filter movies based on directors
    director_movies = directors_df[directors_df['primaryName'].isin(directors)]
    # get the movies from column knownForTitles and split them into a list
    director_movies = director_movies['knownForTitles'].str.split(',').tolist()
    # get all movies from movies_df that are in the list of director_movies
    director_movies = movies_df[movies_df['tconst'].isin([item for sublist in director_movies for item in sublist])]


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
    rated_movies = movies_df[movies_df['primaryTitle'].isin(preferred_movies.keys())]
    # add the ratings to the rated_movies
    rated_movies['rating'] = rated_movies['primaryTitle'].map(preferred_movies)



    ### Above part is good, below needs further work



    # TODO split on knownForTitles and then merge with movies_df probably or implement by hand instead of using libs
    # Merge additional information (like actors and directors) into recommended_movies so that each movie has corresponding attributes that can be used for content-based filtering.
    recommended_movies = recommended_movies.merge(directors_df, on='knownForTitles', how='left')
    recommended_movies = recommended_movies.merge(actors_df, on='knownForTitles', how='left')

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