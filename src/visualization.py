import plotly.express as px
import streamlit as st


# ============================================
# Module 15: Interactive Content Distribution
# ============================================

def show_content_distribution(filtered_df):

    content_counts = (
        filtered_df["type"]
        .value_counts()
    )

    fig = px.pie(
        values=content_counts.values,
        names=content_counts.index,
        title="Netflix Content Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================
# Module 16: Top Genre Analytics
# ============================================

def show_genre_analysis(filtered_df):

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