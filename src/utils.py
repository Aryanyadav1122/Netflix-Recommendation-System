import streamlit as st


# ============================================
# Module 14: Dashboard Metrics Utility
# ============================================

def show_dashboard_metrics(df):

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Titles",
            len(df)
        )

    with col2:
        st.metric(
            "Movies",
            len(df[df["type"] == "Movie"])
        )

    with col3:
        st.metric(
            "TV Shows",
            len(df[df["type"] == "TV Show"])
        )


# ============================================
# Module 18: Recommendation Explanation Utility
# ============================================

def show_recommendation_reason(
    selected_data,
    movie
):

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

        • Shared Genres:
        {", ".join(list(shared_genres)[:3])}

        • Shared Cast:
        {", ".join(list(shared_cast)[:3])}
        """
    )


# ============================================
# Module 23: Footer Utility
# ============================================

def show_footer():

    st.markdown("---")

    st.markdown(
        "Made with ❤️ using Python, "
        "Streamlit, and Machine Learning"
    )