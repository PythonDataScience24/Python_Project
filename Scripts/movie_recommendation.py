import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Task 1: Movie Input and Preferences
def get_user_input():
    watched_movies = {}
    while True:
        movie_title = input("Enter a movie title (or type 'done' to finish): ")
        if movie_title.lower() == 'done':
            break
        rating = float(input("Rate the movie (1-5): "))
        watched_movies[movie_title] = rating
    favorite_genres = input("Enter your favorite genres (comma-separated): ").split(',')
    return watched_movies, favorite_genres

# Task 2: Movie Recommendation Algorithm
def recommend_movies(watched_movies, favorite_genres, movie_data):
    user_profile = pd.Series(0, index=movie_data.columns)
    matching_movies = []
    for movie, rating in watched_movies.items():
        if movie in movie_data.index:
            matching_movies.append(movie)
            numeric_columns = movie_data.select_dtypes(include=['int', 'float']).columns
            user_profile[numeric_columns] += movie_data.loc[movie, numeric_columns] * rating
    
    if not matching_movies:
        print("No matching movies found in the dataset. Please enter more movies.")
        return None

    # Filter movies by favorite genres
    relevant_movies = movie_data[movie_data['genre'].apply(lambda x: any(genre.lower() in x.lower() for genre in favorite_genres))]
    
    # Calculate similarity between user profile and each movie
    similarities = cosine_similarity([user_profile], relevant_movies.select_dtypes(include=['int', 'float']).values)

    # Get indices of top recommended movies
    indices = similarities.argsort()[0][-5:][::-1]

    recommended_movies = relevant_movies.iloc[indices]
    return recommended_movies

# Task 3: Data Visualization and User Trend Analysis
def visualize_data(watched_movies, movie_data):
    # Visualization of user's watched movies
    watched_movies_df = pd.DataFrame(watched_movies.items(), columns=['Movie', 'Rating'])
    print("User's watched movies:")
    print(watched_movies_df)

    # Visualization of breakdown of movies by genre
    genre_counts = movie_data['genre'].apply(lambda x: pd.Series(x.split(','))).stack().value_counts()
    print("\nBreakdown of movies by genre:")
    print(genre_counts)

    # Visualization of breakdown of movies by actor
    actor_counts = movie_data['actors'].apply(lambda x: pd.Series(x.split(','))).stack().value_counts()
    print("\nBreakdown of movies by actor:")
    print(actor_counts)

    # Visualization of breakdown of movies by director
    director_counts = movie_data['director'].value_counts()
    print("\nBreakdown of movies by director:")
    print(director_counts)

# Sample movie data
movies = {
    'title': ['The Shawshank Redemption', 'The Godfather', 'The Dark Knight', 'Pulp Fiction', 'Forrest Gump'],
    'genre': ['Drama', 'Crime, Drama', 'Action, Crime, Drama', 'Crime, Drama', 'Drama, Romance'],
    'actors': ['Tim Robbins, Morgan Freeman', 'Marlon Brando, Al Pacino', 'Christian Bale, Heath Ledger', 'John Travolta, Uma Thurman', 'Tom Hanks, Robin Wright'],
    'director': ['Frank Darabont', 'Francis Ford Coppola', 'Christopher Nolan', 'Quentin Tarantino', 'Robert Zemeckis']
}

movie_data = pd.DataFrame(movies)
movie_data.set_index('title', inplace=True)

# Main program
def main():
    print("Welcome to the Movie Recommendation System!")
    watched_movies, favorite_genres = get_user_input()
    recommended_movies = recommend_movies(watched_movies, favorite_genres, movie_data)
    if recommended_movies is not None:
        print("\nRecommended Movies:")
        print(recommended_movies)
        visualize_data(watched_movies, movie_data)

if __name__ == "__main__":
    main()
