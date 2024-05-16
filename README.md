# Python_Project: Movie Recommendation System

This project is designed to help discover new movies tailored to the users preferences. Users can input movies they have watched along with rating, and specify their favorite genres, actors or directors to personalize their recommendations. 

## Features 
- **Movie Input Preferences**: Users can input movies they have watched and rate them. Moreover, they can specify favorite genre, etc.

- **Recommendation Algorithm**: The system employs a basic recommendation algorithm to suggest new movies based on user preferences and ratings. Recommended movies are displayed along with their details.

- **Data Visualization and User Trend Analysis**: Users are provided with visualizations of their movie data, including breakdonws by genre, actor or director. This allows users to analyze trends in their movie preferences and discover new content.

This project aims to enhance movie-watching experience by offering personalized recommendations and insights into the users' movie preferences. 

## Usage

Make sure to check dependencies before beginning: `pip install -r requirements.txt`  

This project functions as a Dash app. To get started, simply run `python3 app.py` and visit `127.0.0.1:8050` or `localhost:8050` in a web browser.  

For the first week, we created the inital app and its search functionality. It currently consists of several dropdowns, which allow you to search for and select favorite movies, actors, directors, and genres, and a submission button. Once submitted, these data are currently displayed as text output on the page, but will later be fed into the movie recommendation algorithm (needs to be completed) and the results visualized below on the app. In addition, the basic movie recommendation algorithm was developed (in `Scripts/movie_recommendationv2.py`), which, in the future, we will call from inside the app with user data.  

In the second week, additional development included `get_data.py`, intended to download the relevant database via IMDb. Hence, the input of the user will be used to make recommendations based on this data set. This data download proceeds automatically upon launching the app and creates a data folder (these files should not be hosted on github, so ./data is in .gitignore); it may take a minute to download, please be patient! We also created movie recommendation scripts to be invoked by the app to recommend movies based on the input data. 
