# ============================================
# Module 0: Import Required Libraries
# ============================================

import re
import time
import pandas as pd
import streamlit as st
from src.config import *
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


show_dashboard_metrics(df)

show_content_distribution(filtered_df)

show_genre_analysis(filtered_df)

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

                    st.markdown(
                        f"## 🎬 {movie['title']}"
                    )

                    st.progress(
                        min(movie["match_score"] / 100, 1.0)
                    )

                    st.success(
                        f"🎯 Match Confidence: {movie['match_score']}%"
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
                    st.caption(
                        "Content similarity generated using hybrid NLP embeddings"
                    )
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