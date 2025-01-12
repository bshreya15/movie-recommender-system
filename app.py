import streamlit as st
import pickle
import requests
from style import set_custom_css
from dotenv import dotenv_values

# Apply custom styles
set_custom_css()

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

# load pickle files
movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

# web page title
hcol1, hcol2, hcol3 = st.columns(3)

with hcol1:
    st.image("./img1.webp", width=85, use_column_width=None,
             clamp=False, channels="RGB", output_format="auto", use_container_width=False)
with hcol2:
    st.title('Showtime!')

st.markdown("### Find similar movies for your next  binge adventure")

# movie list dropdown
selected_movie_name = st.selectbox(
    'Select Movie',
    movies_list['title'].values
)

# onClick recommend button
if st.button('Recommend'):

    # call recommend function for selected movie
    names, posters = recommend(selected_movie_name)

    # create col using streamlit
    col1, col2, col3, col4, col5 = st.columns(5, vertical_alignment="top", )

    # Loop through the columns and display the image and name
    for i, col in enumerate([col1, col2, col3, col4, col5], start=1):
        with col:
            st.image(posters[i - 1])  # Display the image
            st.text(names[i - 1])  # Display the name