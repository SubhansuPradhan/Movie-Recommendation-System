import pickle
import streamlit as st
import requests

background_image_url = "https://i.postimg.cc/13w7BZ1H/It-s-Movie-Time-1.gif"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;

        height: 100vh;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
        font-family: bree serif; 
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=edfcd7f362b3635c22246f7e25652a6f"
    try:
        response = requests.get(url, timeout=30)
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')
    except:
        return "https://via.placeholder.com/200x300?text=Poster+Not+Found"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])
    return [
        (movies.iloc[i[0]].title, fetch_poster(movies.iloc[i[0]].movie_id))
        for i in distances[1:11]
    ]


movies = pickle.load(open('artificats/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artificats/similary.pkl', 'rb'))


st.title("📽Movie Recommendation System")
st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

selected_movie = st.selectbox(
    "🍿Search for a movie:",
    movies['title'].values,
    help="Start typing to search from 5000 movies"
)

if st.button("Get Recommendations 📽"):
    with st.spinner("Fetching recommendations..."):
        recommendations = recommend(selected_movie)
    
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommendations[i][1])
            st.text(f"{recommendations[i][0]}")
      
    cols = st.columns(5)
    for i in range(5, 10):
        with cols[i-5]:
            st.image(recommendations[i][1])
            st.text(f"{recommendations[i][0]}")