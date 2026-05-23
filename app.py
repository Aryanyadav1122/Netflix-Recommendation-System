# ============================================
# Module 0: Import Required Libraries
# ============================================

import re
import time
import pandas as pd
import streamlit as st
import plotly.express as px

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer
)

from sklearn.metrics.pairwise import cosine_similarity


# ============================================
# Module 1: Streamlit Page Configuration
# ============================================

st.set_page_config(
    page_title="Netflix Recommendation System",
    page_icon="🎬",
    layout="wide"
)


# ============================================
# Module 2: Custom Netflix UI Styling
# ============================================

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


# ============================================
# Module 3: Sidebar Filters
# ============================================

st.sidebar.title("Filters")

content_type = st.sidebar.selectbox(
    "Choose Content Type",
    ["All", "Movie", "TV Show"]
)
num_recommendations = st.sidebar.slider(
    "Number of Recommendations",
    min_value=1,
    max_value=10,
    value=5
)


# ============================================
# Module 4: Dataset Loading
# ============================================

@st.cache_data
def load_data():
    return pd.read_csv("data/netflix_titles.csv")


df = load_data()


# ============================================
# Module 5: Missing Value Handling
# ============================================

df["description"] = df["description"].fillna("")
df["listed_in"] = df["listed_in"].fillna("")
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")


# ============================================
# Module 6: Advanced Text Normalization
# ============================================

def clean_data(text):

    if isinstance(text, str):

        text = text.lower()

        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    return ""


df["listed_in"] = df["listed_in"].apply(clean_data)
df["description"] = df["description"].apply(clean_data)
df["director"] = df["director"].apply(clean_data)
df["cast"] = df["cast"].apply(clean_data)
df["country"] = df["country"].apply(clean_data)


# ============================================
# Module 7: Dataset Filtering
# ============================================

if content_type != "All":
    filtered_df = df[df["type"] == content_type]
else:
    filtered_df = df


# ============================================
# Module 8: Weighted Feature Engineering
# ============================================

features = (
    df["listed_in"] * 3 + " " +
    df["cast"] * 2 + " " +
    df["director"] * 2 + " " +
    df["description"] + " " +
    df["country"]
)


# ============================================
# Module 9: Hybrid Vectorization Engine
# ============================================

@st.cache_resource
def create_vectors(features):

    # TF-IDF Vectorization
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(features)

    # CountVectorizer Embeddings
    count_vectorizer = CountVectorizer(stop_words="english")
    count_matrix = count_vectorizer.fit_transform(features)

    return tfidf_matrix, count_matrix


tfidf_matrix, count_matrix = create_vectors(features)


# ============================================
# Module 10: Hybrid Similarity Computation
# ============================================

cosine_sim = cosine_similarity(tfidf_matrix)

count_sim = cosine_similarity(count_matrix)


# ============================================
# Module 11: Title Index Mapping
# ============================================

indices = pd.Series(
    df.index,
    index=df["title"]
).drop_duplicates()


# ============================================
# Module 12: Hybrid Recommendation Engine
# ============================================

def recommend(title):

    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    # TF-IDF Similarity Scores
    tfidf_scores = cosine_sim[idx]

    # CountVectorizer Similarity Scores
    count_scores = count_sim[idx]

    # Hybrid Similarity Fusion
    # Module 20: Genre-Aware Similarity Boosting

    hybrid_scores = (tfidf_scores + count_scores) / 2

    selected_genres = set(
        df.iloc[idx]["listed_in"].split()
    )

    for i in range(len(hybrid_scores)):

        movie_genres = set(
            df.iloc[i]["listed_in"].split()
        )

        common_genres = (
            selected_genres.intersection(movie_genres)
        )

        hybrid_scores[i] += len(common_genres) * 0.01

    sim_scores = list(enumerate(hybrid_scores))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )
    # Module 12.1: Recommendation Diversity Filtering

    unique_titles = set()

    filtered_scores = []

    for score in sim_scores:

        movie_title = df.iloc[score[0]]["title"]

        if movie_title not in unique_titles:

            unique_titles.add(movie_title)

            filtered_scores.append(score)

    sim_scores = filtered_scores

    sim_scores = sim_scores[
        1:num_recommendations + 1
    ]

    movie_indices = [i[0] for i in sim_scores]

    scores = [i[1] for i in sim_scores]

    recommended_movies = df.iloc[movie_indices].copy()

    recommended_movies["match_score"] = [
        round(score * 100, 2)
        for score in scores
    ]

    return recommended_movies


# ============================================
# Module 13: Main Dashboard UI
# ============================================

st.title("🎬 Netflix Recommendation System")

st.markdown(
    "Discover Movies and TV Shows Similar to Your Favorites"
)


# ============================================
# Module 14: Dashboard Metrics
# ============================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Titles", len(df))

with col2:
    st.metric("Movies", len(df[df["type"] == "Movie"]))

with col3:
    st.metric("TV Shows", len(df[df["type"] == "TV Show"]))

# ============================================
# Module 15: Interactive Content Distribution
# ============================================

content_counts = filtered_df["type"].value_counts()

fig = px.pie(
    values=content_counts.values,
    names=content_counts.index,
    title="Netflix Content Distribution"
)

st.plotly_chart(fig, use_container_width=True)
# ============================================
# Module 16: Top Genre Analytics
# ============================================

top_genres = (
    filtered_df["listed_in"]
    .value_counts()
    .head(10)
)

fig = px.bar(
    x=top_genres.values,
    y=top_genres.index,
    orientation="h",
    title="Top 10 Netflix Genres"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# ============================================
# Module 17: Content Selection Interface
# ============================================

selected_movie = st.selectbox(
    "🔍 Search and Select a Movie or TV Show",
    sorted(filtered_df["title"].unique())
)


# ============================================
# Module 18: Recommendation Generation Workflow
# ============================================

if st.button("Recommend"):

    with st.spinner("Finding best recommendations..."):

        time.sleep(2)

        recommendations = recommend(selected_movie)

        if recommendations.empty:

            st.error("No recommendations found")

        else:

            st.success(
                "Recommendations Generated Successfully"
            )

            st.subheader("Recommended Content")

            st.write(
                f"Showing {len(recommendations)} recommendations"
            )

            # ============================================
            # Module 19: Recommendation Display Cards
            # ============================================

            for _, movie in recommendations.iterrows():

                with st.container():

                    st.markdown(
                        f"## 🎬 {movie['title']}"
                    )

                    st.progress(
                        min(movie["match_score"] / 100, 1.0)
                    )

                    st.write(
                        f"🎯 Match Score: {movie['match_score']}%"
                    )
                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("📺 Type:", movie["type"])
                        st.write(
                            "📅 Release Year:",
                            movie["release_year"]
                        )
                        st.write(
                            "🌍 Country:",
                            movie["country"]
                        )

                    with col2:
                        st.write(
                            "🎭 Genre:",
                            movie["listed_in"]
                        )
                        st.write(
                            "⭐ Rating:",
                            movie["rating"]
                        )
                        st.write(
                            "🎬 Director:",
                            movie["director"]
                        )

                    st.write("🧑 Cast:", movie["cast"])
                    selected_data = df[
                        df["title"] == selected_movie
                    ].iloc[0]

                    shared_genres = set(
                        selected_data["listed_in"].split()
                    ).intersection(
                        set(movie["listed_in"].split())
                    )                   

                    shared_cast = set(
                        selected_data["cast"].split()
                    ).intersection(
                        set(movie["cast"].split())
                    )

                    st.info(
                        f"""
                        Recommended because of:
    
                        • Shared Genres: {", ".join(list(shared_genres)[:3])}
    
                        • Shared Cast: {", ".join(list(shared_cast)[:3])}
                        """
                    )

                    with st.expander(
                        "📝 Show Description"
                    ):
                        st.write(movie["description"])

                    st.markdown("---")


# ============================================
# Module 20: Footer Section
# ============================================

st.markdown("---")

st.markdown(
    "Made with ❤️ using Python, Streamlit, and Machine Learning"
)