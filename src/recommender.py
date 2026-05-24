import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer
)

from sklearn.metrics.pairwise import cosine_similarity


# ============================================
# Module 8: Weighted Feature Engineering
# ============================================

def create_features(df):

    features = (
        df["listed_in"] * 3 + " " +
        df["cast"] * 2 + " " +
        df["director"] * 2 + " " +
        df["description"] + " " +
        df["country"]
    )

    return features


# ============================================
# Module 9: Hybrid Vectorization Engine
# ============================================

@st.cache_resource
def create_vectors(features):

    tfidf = TfidfVectorizer(stop_words="english")

    tfidf_matrix = tfidf.fit_transform(features)

    count_vectorizer = CountVectorizer(
        stop_words="english"
    )

    count_matrix = count_vectorizer.fit_transform(
        features
    )

    return tfidf_matrix, count_matrix


# ============================================
# Module 10: Hybrid Similarity Computation
# ============================================

def compute_similarity(features):

    tfidf_matrix, count_matrix = create_vectors(
        features
    )

    cosine_sim = cosine_similarity(tfidf_matrix)

    count_sim = cosine_similarity(count_matrix)

    return cosine_sim, count_sim


# ============================================
# Module 12: Hybrid Recommendation Engine
# ============================================

def recommend(
    title,
    df,
    cosine_sim,
    count_sim,
    indices,
    num_recommendations
):

    if title not in indices:
        return pd.DataFrame()

    idx = indices[title]

    tfidf_scores = cosine_sim[idx]

    count_scores = count_sim[idx]

    # Module 20: Genre-Aware Similarity Boosting

    hybrid_scores = (
        tfidf_scores + count_scores
    ) / 2

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

        hybrid_scores[i] += (
            len(common_genres) * 0.01
        )

    sim_scores = list(
        enumerate(hybrid_scores)
    )

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Module 19.1:
    # Recommendation Diversity Filtering

    unique_titles = set()

    filtered_scores = []

    for score in sim_scores:

        movie_title = df.iloc[
            score[0]
        ]["title"]

        if movie_title not in unique_titles:

            unique_titles.add(movie_title)

            filtered_scores.append(score)

    sim_scores = filtered_scores

    sim_scores = sim_scores[
        1:num_recommendations + 1
    ]

    movie_indices = [i[0] for i in sim_scores]

    scores = [i[1] for i in sim_scores]

    recommended_movies = df.iloc[
        movie_indices
    ].copy()

    recommended_movies["match_score"] = [
        round(score * 100, 2)
        for score in scores
    ]

    return recommended_movies