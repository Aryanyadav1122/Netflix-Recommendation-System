# ============================================
# Module 0: Import Required Libraries
# ============================================

import re
import time
import pandas as pd
import streamlit as st

from src.config import *
from src.tmdb_api import (
    fetch_movie_data,
    fetch_trending_movies
)

from src.preprocessing import (
    handle_missing_values,
    preprocess_text
)

from src.recommender import (
    create_features,
    compute_similarity,
    recommend
)

from src.visualization import (
    show_content_distribution,
    show_genre_analysis
)

from src.utils import (
    show_dashboard_metrics,
    show_recommendation_reason,
    show_footer
)


# ============================================
# Module 1: Streamlit Page Configuration
# ============================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT
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
    /* Recommendation Card Styling */

    .recommend-card {
        background-color: #1f1f1f;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        border: 1px solid #333;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
        transition: 0.3s;
    }

    .recommend-card:hover {
        transform: scale(1.01);
        border: 1px solid #E50914;
    }

    .match-score {
        color: #00ff95;
        font-weight: bold;
        font-size: 18px;
    }

    .movie-title {
        color: #E50914;
        font-size: 28px;
        font-weight: bold;
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
    max_value=MAX_RECOMMENDATIONS,
    value=DEFAULT_RECOMMENDATIONS
)


# ============================================
# Module 4: Dataset Loading
# ============================================

@st.cache_data
def load_data():
    return pd.read_csv("data/netflix_titles.csv")


df = load_data()

df = handle_missing_values(df)

df = preprocess_text(df)

features = create_features(df)

cosine_sim, count_sim = compute_similarity(
    features
)

indices = pd.Series(
    df.index,
    index=df["title"]
).drop_duplicates()


# ============================================
# Module 7: Dataset Filtering
# ============================================

if content_type != "All":
    filtered_df = df[df["type"] == content_type]
else:
    filtered_df = df


# ============================================
# Module 11: Title Index Mapping
# ============================================

indices = pd.Series(
    df.index,
    index=df["title"]
).drop_duplicates()


# ============================================
# Module 13: Main Dashboard UI
# ============================================

st.title("🎬 Netflix Recommendation System")

st.markdown(
    APP_DESCRIPTION
)

st.info(
    """
    🔥 Features Included:

    • Hybrid Recommendation Engine

    • TF-IDF + CountVectorizer NLP

    • Interactive Analytics Dashboard

    • Explainable AI Recommendations

    • Genre-Aware Ranking Optimization
    """
)


# ============================================
# Module 30: Trending Movies Dashboard
# ============================================

st.subheader("🔥 Trending Movies This Week")

trending_movies = fetch_trending_movies()

trend_cols = st.columns(5)

for idx, movie in enumerate(trending_movies[:5]):

    with trend_cols[idx]:

        poster_path = movie.get("poster_path")

        if poster_path:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

            st.image(poster_url)

        st.caption(movie["title"])


show_dashboard_metrics(df)

show_content_distribution(filtered_df)

show_genre_analysis(filtered_df)


# ============================================
# Module 17: Content Selection Interface
# ============================================

movie_titles = sorted(
    filtered_df["title"].dropna().unique()
)

selected_movie = st.selectbox(
    "🔍 Search Movie or TV Show",
    movie_titles
)
# ============================================
# Module 18: Recommendation Generation Workflow
# ============================================

if st.button("Recommend") and selected_movie:

    with st.spinner("Finding best recommendations..."):

        st.toast(
            "Building hybrid recommendation engine..."
        )

        time.sleep(2)

        st.toast(
            "Applying similarity ranking and personalization..."
        )

        recommendations = recommend(
            selected_movie,
            df,
            cosine_sim,
            count_sim,
            indices,
            num_recommendations
        )

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

                    movie_data_tmdb = fetch_movie_data(
                        movie["title"]
                    )
                    # Main Layout Columns
                    poster_col, details_col = st.columns([1, 2])

                    # ============================================
                    # Left Section: Movie Poster
                    # ============================================

                    with poster_col:

                        if movie_data_tmdb and movie_data_tmdb.get("poster"):

                            st.image(
                                movie_data_tmdb["poster"],
                                width=250
                            )

                        else:

                            st.image(
                                "https://via.placeholder.com/250x375?text=No+Image",
                                width=250
                            )

                    # ============================================
                    # Right Section: Movie Details
                    # ============================================

                    with details_col:

                        st.markdown(
                            f"## 🎬 {movie['title']}"
                        )

                        if movie_data_tmdb:

                            rating = movie_data_tmdb["rating"]

                            stars = "⭐" * int(rating // 2)

                            st.markdown(
                                f"""
                                <div class="match-score">
                                    {stars} {rating}/10
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            st.write(
                                "🔥 Popularity:",
                                round(
                                    movie_data_tmdb["popularity"],
                                    2
                                )
                            )

                            st.write(
                                "📅 TMDB Release Date:",
                                movie_data_tmdb["release_date"]
                            )

                        st.progress(
                            min(movie["match_score"] / 100, 1.0)
                        )

                        match_score = movie["match_score"]

                        if match_score >= 80:
                            confidence = "Excellent Match"

                        elif match_score >= 60:
                            confidence = "Very Good Match"

                        elif match_score >= 40:
                            confidence = "Good Match"

                        else:
                            confidence = "Average Match"

                        st.markdown(
                            f"""
                            <div class="match-score">
                                🎯 {confidence} — {match_score}%
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        info_col1, info_col2 = st.columns(2)

                        with info_col1:

                            st.write(
                                "📺 Type:",
                                movie["type"]
                            )

                            st.write(
                                "📅 Release Year:",
                                movie["release_year"]
                            )

                            st.write(
                                "🌍 Country:",
                                movie["country"]
                            )

                        with info_col2:

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

                        st.write(
                            "🧑 Cast:",
                            movie["cast"]
                        )

                        st.caption(
                            "Content similarity generated using hybrid NLP embeddings"
                        )

                        selected_data = df[
                            df["title"] == selected_movie
                        ].iloc[0]

                        show_recommendation_reason(
                            selected_data,
                            movie
                        )

                        with st.expander(
                            "📝 Show Description"
                        ):

                            st.write(
                                movie["description"]
                            )
                    st.markdown(
                        '<div class="recommend-card">',
                        unsafe_allow_html=True
                    )
                    st.markdown("---")


# ============================================
# Module 20: Footer Section
# ============================================

st.markdown("---")

st.markdown(
    "Made with ❤️ using Python, Streamlit, and Machine Learning"
)