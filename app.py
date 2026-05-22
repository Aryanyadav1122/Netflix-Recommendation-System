import pandas as pd
import streamlit as st
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.markdown(
    """
    <style>

    .stApp {
        background-color: #141414;
        color: white;
    }

    h1, h2, h3 {
        color: #E50914;
    }

    .stButton > button {
        background-color: #E50914;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 18px;
        border: none;
    }

    .stSelectbox label {
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# Page Config
st.set_page_config(
    page_title="Netflix Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# Sidebar
st.sidebar.title("Filters")

content_type = st.sidebar.selectbox(
    "Choose Content Type",
    ["All", "Movie", "TV Show"]
)

# Load Dataset
df = pd.read_csv("data/netflix_titles.csv")

# Handle Missing Values
df["description"] = df["description"].fillna("")
df["listed_in"] = df["listed_in"].fillna("")
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")

# Filter Dataset
if content_type != "All":
    filtered_df = df[df["type"] == content_type]
else:
    filtered_df = df

# Combine Features
features = df["listed_in"] + " " + df["description"]

# Convert Text to Numerical Vectors
tfidf = TfidfVectorizer(stop_words="english")

tfidf_matrix = tfidf.fit_transform(features)

# Similarity Matrix
cosine_sim = cosine_similarity(tfidf_matrix)

# Create Title Index Mapping
indices = pd.Series(df.index, index=df["title"]).drop_duplicates()

# Recommendation Function
def recommend(title):

    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    sim_scores = sim_scores[1:6]

    movie_indices = [i[0] for i in sim_scores]

    return df.iloc[movie_indices]

# Main Title
st.title("🎬 Netflix Recommendation System")

st.markdown(
    "Discover Movies and TV Shows Similar to Your Favorites"
)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Titles", len(df))

with col2:
    st.metric("Movies", len(df[df["type"] == "Movie"]))

with col3:
    st.metric("TV Shows", len(df[df["type"] == "TV Show"]))

# Movie Selection
selected_movie = st.selectbox(
    "🔍 Search and Select a Movie or TV Show",
    sorted(filtered_df["title"].unique())
)

# Recommendation Button
if st.button("Recommend"):

    with st.spinner("Finding best recommendations..."):

        time.sleep(2)

        st.success("Recommendations Generated Successfully")

        recommendations = recommend(selected_movie)
        if recommendations.empty:
            st.error("No recommendations found")
            st.subheader("Recommended Content")

        st.subheader("Recommended Content")
        st.write(f"Showing {len(recommendations)} recommendations")

        for _, movie in recommendations.iterrows():

            with st.container():

                st.markdown(f"## 🎬 {movie['title']}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("📺 Type:", movie["type"])
                    st.write("📅 Release Year:", movie["release_year"])
                    st.write("🌍 Country:", movie["country"])

                with col2:
                    st.write("🎭 Genre:", movie["listed_in"])
                    st.write("⭐ Rating:", movie["rating"])
                    st.write("🎬 Director:", movie["director"])

                st.write("🧑 Cast:", movie["cast"])

                with st.expander("📝 Show Description"):
                    st.write(movie["description"])

                st.markdown("---")
                st.markdown("---")

                st.markdown(
                        "Made with ❤️ using Python, Streamlit, and Machine Learning"
                )