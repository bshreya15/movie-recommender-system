import streamlit as st
import pickle
import requests
from dotenv import dotenv_values
keys = dotenv_values(".env")

# function to fetch posters of similar movies
def fetch_poster(movie_id):
    img_path_prefix = "https://image.tmdb.org/t/p/w500"

    url = "https://api.themoviedb.org/3/movie/{}?language=en-US".format(movie_id)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(keys["tmdb_api_key"])
    }

    # API request for a movie_id
    resp = requests.get(url , headers = headers)
    data = resp.json()

    # return poster_path from JSON data object
    return img_path_prefix + data['poster_path']

# function to recommend similar movies
def recommend(movie):
    # find index of selected movie in df
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    # find the similarity row of selected movie
    distances = similarity[movie_index]
    # sort similarity distances in decreasing order
    # store top 5 similar movies in list
    movies_rec = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    # store titles of top similar movies
    recommended_movies = []

    # store poster_path of top similar movies
    recommended_movies_posters = []

    for i in movies_rec:
        # find movie_id
        movie_id = movies_list.iloc[i[0]].movie_id

        # fetch similar movie posters
        recommended_movies_posters.append(fetch_poster(movie_id))

        # fetch similar movie titles
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters


movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select Movie',
    movies_list['title'].values
)

if st.button('Recommend'):
    movies = recommend(selected_movie_name)
    for movie in movies:
        st.text(movie)