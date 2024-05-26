# Python_Project: Movie Recommendation System

This project is designed to help discover new movies tailored to the users preferences. Users can input movies they have watched along with rating, and specify their favorite genres, actors or directors to personalize their recommendations. 

## Features 
- **Movie Input Preferences**: Users can input movies they have watched and rate them. Moreover, they can specify favorite genre, etc.

- **Recommendation Algorithm**: The system employs a basic recommendation algorithm to suggest new movies based on user preferences and ratings. Recommended movies are displayed along with their details.

- **Data Visualization and User Trend Analysis**: Users are provided with visualizations of their movie data, including breakdonws by genre, actor or director. This allows users to analyze trends in their movie preferences and discover new content.

This project aims to enhance movie-watching experience by offering personalized recommendations and insights into the users' movie preferences. 

## Usage

Make sure (1) virtualenv is installed, (2) create a virtual environment, and (3) activate the virtual environment before beginning: 
1. `pip show virtualenv`/`which virtualenv`, and `pip install virtualenv` if required
2. `virtualenv venv`
3. `source venv/bin/activate`  
Then, install the necessary dependencies from within the environment: 
4. `pip install -r requirements.txt`  

This project functions as a Dash app. To get started, simply run `python3 app.py` and visit `127.0.0.1:8050` or `localhost:8050` in a web browser.  

For the first week, we created the inital app and its search functionality. It currently consists of several dropdowns, which allow you to search for and select favorite movies, actors, directors, and genres, and a submission button. Once submitted, these data are currently displayed as text output on the page, but will later be fed into the movie recommendation algorithm (needs to be completed) and the results visualized below on the app. In addition, the basic movie recommendation algorithm was developed (in `Scripts/movie_recommendationv2.py`), which, in the future, we will call from inside the app with user data.  

In the second week, additional development included `get_data.py`, intended to download the relevant database via IMDb. Hence, the input of the user will be used to make recommendations based on this data set. The data obtained from running the script are provided in the `data` folder as compressed tsv files. We also created movie recommendation scripts to be invoked by the app to recommend movies based on the input data.

In the third week we completed our recommendation algorithm and included two plots to visualize the recommended movies. First we show the Top 10 
recommendations in a bar plot with their indices in the DataFrame. The recommendations go from place 1 (left) to place 10 (right) independent of the size of the bar. We still would like to exchange the index on the y-axis with the actual value given to each movie by the cosine similarities from our recommendation algorithm. We also included a pie chart to show the distribution of genres of the Top 10 recommended movies.

In the fourth week we initialized a virtual environment for the project to containerize the dependencies of the app away from the user's main environment, and included instructions how to start the container and install the required packages.
