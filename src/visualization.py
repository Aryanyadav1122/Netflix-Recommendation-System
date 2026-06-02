import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


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
# Module 33: Rating Distribution Analysis
# ============================================

def show_rating_distribution(df):

    st.subheader("⭐ Rating Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.histplot(
        df["rating"].dropna(),
        bins=20,
        ax=ax
    )

    ax.set_title(
        "Distribution of Ratings"
    )

    st.pyplot(fig)

# ============================================
# Module 34: Correlation Analysis
# ============================================

def show_correlation_heatmap(df):

    st.subheader("📊 Correlation Analysis")

    numeric_df = df[
        ["rating", "popularity"]
    ].copy()

    corr_matrix = numeric_df.corr()

    fig, ax = plt.subplots(
        figsize=(6, 4)
    )

    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="Blues",
        ax=ax
    )

    ax.set_title(
        "Feature Correlation Heatmap"
    )

    st.pyplot(fig)

# ============================================
# Module 35: Popularity vs Rating Analysis
# ============================================

def show_popularity_vs_rating(df):

    st.subheader(
        "🔥 Popularity vs Rating"
    )

    fig, ax = plt.subplots(
        figsize=(8, 5)
    )

    sns.scatterplot(
        data=df,
        x="popularity",
        y="rating",
        ax=ax
    )

    ax.set_title(
        "Popularity vs Rating"
    )

    st.pyplot(fig)


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