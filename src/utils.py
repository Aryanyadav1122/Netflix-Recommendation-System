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
        str(selected_data["listed_in"]).split(",")
    ).intersection(
        set(str(movie["listed_in"]).split(","))
    )

    shared_cast = set(
        str(selected_data["cast"]).split(",")
    ).intersection(
        set(str(movie["cast"]).split(","))
    )

    st.markdown(
        """
        <div style="margin-top:10px; margin-bottom:15px;">
        """,
        unsafe_allow_html=True
    )

    if shared_genres:

        for genre in list(shared_genres)[:3]:

            st.markdown(
                f"""
                <span style="
                    background-color:#E50914;
                    padding:6px 12px;
                    border-radius:20px;
                    margin-right:8px;
                    color:white;
                    font-size:14px;
                ">
                🎭 {genre.strip()}
                </span>
                """,
                unsafe_allow_html=True
            )

    if shared_cast:

        for actor in list(shared_cast)[:3]:

            st.markdown(
                f"""
                <span style="
                    background-color:#333;
                    padding:6px 12px;
                    border-radius:20px;
                    margin-right:8px;
                    color:white;
                    font-size:14px;
                ">
                🎬 {actor.strip()}
                </span>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        """
        <span style="
            background-color:#444;
            padding:6px 12px;
            border-radius:20px;
            margin-right:8px;
            color:white;
            font-size:14px;
        ">
        🤖 NLP Match
        </span>
        </div>
        """,
        unsafe_allow_html=True
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