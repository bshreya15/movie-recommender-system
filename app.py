import streamlit as st
import pickle


movies_list = pickle.load(open('movies.pkl','rb'))

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select Movie',
    movies_list['title'].values
)

