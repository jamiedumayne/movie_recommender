# Movie Recommender
This code recommends movies to watch using the movie rating website letterboxd.com

It uses data science to compare my movie ratings to other user ratings. Then I can find users which ranked movies similar to me, and return the movies that they rated highly which I haven't watched.

# Data
This code uses my data uses from Letterboxd, but could easily use someone else's data. It also uses data provided by Sam Learner, which can be found in their Github: https://github.com/sdl60660/letterboxd_recommendations

# Things to work on
There is somethings I'd like to improve on:
- Use other features to weight suggested movies: year_released, genre, original_language
- Train a machine learning recommender (knn or neural network), however this will need more data from IMDB
- Incorporate just watch api to be able to tailor recommendations based on the streaming platforms I have access to.

There are also some bugs with the code that need fixing
- There is over 4000 users in the data table, this would take a few hours to run. So for now I just limit it to use the first 500 users. 
- Currently a problem with my movie ratings only having the movie title. This means when the data table is merged with the movie data table there is an issue if there is more than one movie with the same name e.g. Cinderella.
- Some movies are missing from the movie table, so if they're recommended from a user's rating I just have to skip those