import streamlit as st
import requests
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Movie Search",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# TMDB API configuration
try:
    TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_URL = "https://image.tmdb.org/t/p/w500"
except KeyError:
    st.error("""
        ⚠️ API Key Missing!
        
        Please configure your TMDB API key:
        1. For local development: Add it to .streamlit/secrets.toml
        2. For Streamlit Cloud: Add it in the Secrets section
        
        The key should be in format:
        [secrets]
        TMDB_API_KEY = "your_api_key_here"
    """)
    st.stop()

# Custom CSS for styling
st.markdown("""
<style>
.stTextInput>div>div>input {
    text-align: center;
    font-size: 18px;
    padding: 12px;
}
.stButton>button {
    width: 100%;
    border-radius: 5px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

def search_movies(query):
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "query": query,
        "language": "en-US",
        "include_adult": "false"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US",
        "append_to_response": "credits"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return None

# Main app
st.title("🎬 Movie Search")
st.markdown("---")

# Search bar
search_term = st.text_input("Enter movie name...", "")

if search_term:
    results = search_movies(search_term)
    
    if results:
        st.markdown(f"**Found {len(results)} results**")
        for movie in results:
            details = get_movie_details(movie["id"])
            if details:
                with st.container():
                    col1, col2 = st.columns([1, 3])
                    
                    with col1:
                        poster_path = details.get("poster_path")
                        if poster_path:
                            st.image(f"{IMAGE_URL}{poster_path}", width=150)
                        else:
                            st.image("https://via.placeholder.com/150x225?text=No+Image", width=150)
                    
                    with col2:
                        st.subheader(details["title"])
                        release_date = details.get("release_date")
                        if release_date:
                            year = datetime.strptime(release_date, "%Y-%m-%d").year
                            st.markdown(f"**Year:** {year}")
                        st.markdown(f"**Rating:** {details['vote_average']}/10")
                        st.markdown(f"**Runtime:** {details['runtime']} mins")
                        if details.get("credits"):
                            cast = details["credits"].get("cast", [])[:3]
                            cast_names = [actor["name"] for actor in cast]
                            st.markdown(f"**Cast:** {', '.join(cast_names)}")
                        st.markdown(details["overview"])
                        st.markdown("---")
    else:
        st.warning("No movies found matching your search")
