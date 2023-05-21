import numpy as np
import pandas as pd
import os

#local directory of data
os.chdir("C:/Users/jamie/Documents/Code/movie_data/")

#import movie data, provided by Sam Learner
#https://github.com/sdl60660/letterboxd_recommendations
movie_info = pd.read_csv('movie_data.csv', lineterminator='\n')
user_rating = pd.read_csv('ratings_export.csv')
user_info = pd.read_csv('users_export.csv')

#drop unnecessary data
movie_info = movie_info.drop(movie_info.columns[[0, 2, 3, 4, 8, 9, 10, 12, 13, 14, 15]],axis = 1)
movie_info = movie_info.fillna(0)
movie_info = movie_info[movie_info["vote_count"] > 5]
movie_info = movie_info[movie_info["year_released"] > 1980]

user_rating = user_rating.drop(user_rating.columns[[0]],axis = 1)
user_info = user_info.drop(user_info.columns[[0, 1]],axis = 1)

#import my ratings, can be replaced for anyones
my_ratings = pd.read_csv('my_ratings.csv')
my_ratings = my_ratings.drop(my_ratings.columns[[0, 3]],axis = 1)
my_ratings["Rating"] = my_ratings["Rating"] * 2
my_ratings["movie_title"] = my_ratings["Name"]

#merge my ratings with movie info, to get movie id for each
movie_join = pd.merge(movie_info, my_ratings, on="movie_title")

#group user reviews by user and get scores
group_user_rating = user_rating.groupby("user_id")

scores = []
user_key_arr = []
user_key = list(group_user_rating.groups.keys())
user_key = user_key[0:100]

for users in user_key:
    user_key_arr.append(users)
    user_score = 0
    
    #get table of ratings for other user
    group_id = group_user_rating.get_group(users)
    for i in range(len(movie_join["movie_id"])):
        #get a movie from my ratings, and get my rating for it
        my_rating_movie_id = movie_join["movie_id"][i]
        my_movie_rating = movie_join["Rating"][i]

        #get index of movie from user reviews
        user_movie_index = group_id.index[group_id['movie_id']==my_rating_movie_id].tolist()
        
        #check if the user has watched the movie
        if user_movie_index:
            user_movie_score = group_id["rating_val"][user_movie_index[0]]
            
            #if their score is within 1 star of mine add 1 to my score
            if user_movie_score <= my_movie_rating+2 and user_movie_score >= my_movie_rating-2:
                #weight the high and low scoring movies more
                if my_movie_rating <=2 or my_movie_rating >=8:
                    user_score = user_score + 5
                else:
                    user_score = user_score + 1

    scores.append(user_score)

#from user scores, return movies that they gave more than 4 stars
num_users = 5

top_users = sorted(range(len(scores)), key=lambda i: scores[i])[-num_users:]

recomendations = []
for i in range(len(top_users)):
    top_user_key = user_key[top_users[i]]
    
    #get the top users highest ranking movie
    top_user_rating = group_user_rating.get_group(top_user_key)
    top_user_rating = top_user_rating[top_user_rating["rating_val"] >= 8]

    count_rec = 0
    movie_rec_id = []
    

    #suggest 2 movies per user
    while count_rec < 2:
        rec_movie = top_user_rating["movie_id"].sample(num_movies)
        rec_movie = rec_movie.values
        in_my_rankings = (movie_join["movie_id"].eq(rec_movie[0])).any()

        if in_my_rankings == False:
            movie_name_id = movie_info.index[movie_info['movie_id'] == rec_movie[0]].tolist()
            
            if movie_name_id:
                recomendations.append(movie_info['movie_title'][movie_name_id])
                count_rec = count_rec + 1


#show recommendation
print("Here's 10 movies you should watch:")
for movie in recomendations:
    print(movie.values[0])