import streamlit as st
import pickle

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
    for i in movies_rec:
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies


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