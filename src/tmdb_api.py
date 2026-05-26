import requests


# ============================================
# Module 28: TMDB API Integration
# ============================================

API_KEY = "b0fe98cc89a85072d43d4997080ec5f4"


def fetch_movie_data(title):

    url = (
        f"https://api.themoviedb.org/3/search/movie"
        f"?api_key={API_KEY}"
        f"&query={title}"
    )

    response = requests.get(url)

    data = response.json()

    if (
        data["results"]
        and len(data["results"]) > 0
    ):

        movie = data["results"][0]

        poster_path = movie.get("poster_path")

        poster_url = None

        if poster_path:

            poster_url = (
                "https://image.tmdb.org/t/p/w500"
                + poster_path
            )

        return {
            "poster": poster_url,
            "rating": movie.get("vote_average"),
            "popularity": movie.get("popularity"),
            "release_date": movie.get("release_date")
        }

    return None
# ============================================
# Module 30: Trending Movies API
# ============================================

def fetch_trending_movies():

    url = (
        f"https://api.themoviedb.org/3/trending/movie/week"
        f"?api_key={API_KEY}"
    )

    response = requests.get(url)

    data = response.json()

    return data["results"][:10]