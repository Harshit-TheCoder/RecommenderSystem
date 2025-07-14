import streamlit as st
import pickle
import requests

st.title('Movie Recommender System (OMDb Version)')

movies_df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies_df['title'].values

  # Replace this with your OMDb API Key

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get("Poster", "")
    return ""

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_lt = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_lt:
        title = movies_df.iloc[i[0]].title
        recommended_movies.append(title)
        recommended_movies_posters.append(fetch_poster(title))
    return recommended_movies, recommended_movies_posters

selected_movie_name = st.selectbox('Please type or select a movie', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    st.write('.........Recommended Movies........')
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            if posters[idx]:
                st.image(posters[idx])
            else:
                st.write("No image found")
            st.text(names[idx])
