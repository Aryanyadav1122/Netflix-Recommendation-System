import requests
import pandas as pd
import time

# ============================================
# Module 31: TMDB Dataset Generator v2
# ============================================

READ_ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiMGZlOThjYzg5YTg1MDcyZDQzZDQ5OTcwODBlYzVmNCIsIm5iZiI6MTc3OTc2MTQ5OS4yMDIsInN1YiI6IjZhMTUwMTViZjQ4NTM5NmFlMDM5NWExOCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.aWh4sG2FIOt8ra1eipQvIPy5tQjYLGZ5FWwBz8YdotM"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {READ_ACCESS_TOKEN}"
}

all_content = []


def fetch_json(url):

    response = requests.get(
        url,
        headers=headers
    )

    return response.json()


def get_director(crew):

    for member in crew:

        if member.get("job") == "Director":

            return member.get("name")

    return "Unknown"


def get_top_cast(cast):

    names = []

    for actor in cast[:5]:

        names.append(actor.get("name"))

    return ", ".join(names)


def get_genres(genres):

    names = []

    for genre in genres:

        names.append(genre.get("name"))

    return ", ".join(names)

def fetch_movie_details(movie_id):

    details_url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
    )

    credits_url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}/credits"
    )

    details = fetch_json(details_url)

    credits = fetch_json(credits_url)

    return {
        "genres": get_genres(
            details.get("genres", [])
        ),
        "cast": get_top_cast(
            credits.get("cast", [])
        ),
        "director": get_director(
            credits.get("crew", [])
        )
    }


def fetch_tv_details(tv_id):

    details_url = (
        f"https://api.themoviedb.org/3/tv/{tv_id}"
    )

    credits_url = (
        f"https://api.themoviedb.org/3/tv/{tv_id}/credits"
    )

    details = fetch_json(details_url)

    credits = fetch_json(credits_url)

    return {
        "genres": get_genres(
            details.get("genres", [])
        ),
        "cast": get_top_cast(
            credits.get("cast", [])
        ),
        "director": "Unknown"
    }
def process_movies():

    for page in range(1, 21):

        print(
            f"Fetching Movie Page {page}"
        )

        url = (
            "https://api.themoviedb.org/3/movie/popular"
            f"?page={page}"
        )

        data = fetch_json(url)

        for movie in data.get("results", []):

            try:

                details = fetch_movie_details(
                    movie["id"]
                )

                all_content.append({

                    "title": movie.get(
                        "title"
                    ),

                    "type": "Movie",

                    "description": movie.get(
                        "overview", ""
                    ),

                    "listed_in": details[
                        "genres"
                    ],

                    "cast": details[
                        "cast"
                    ],

                    "director": details[
                        "director"
                    ],

                    "country": "Unknown",

                    "release_year": (
                        movie.get(
                            "release_date",
                            "0000"
                        )[:4]
                    ),

                    "rating": movie.get(
                        "vote_average"
                    ),

                    "popularity": movie.get(
                        "popularity"
                    )
                })

                time.sleep(0.1)

            except Exception:

                continue

def process_tv_shows():

    for page in range(1, 21):

        print(
            f"Fetching TV Show Page {page}"
        )

        url = (
            "https://api.themoviedb.org/3/tv/popular"
            f"?page={page}"
        )

        data = fetch_json(url)

        for show in data.get("results", []):

            try:

                details = fetch_tv_details(
                    show["id"]
                )

                all_content.append({

                    "title": show.get(
                        "name"
                    ),

                    "type": "TV Show",

                    "description": show.get(
                        "overview", ""
                    ),

                    "listed_in": details[
                        "genres"
                    ],

                    "cast": details[
                        "cast"
                    ],

                    "director": details[
                        "director"
                    ],

                    "country": "Unknown",

                    "release_year": (
                        show.get(
                            "first_air_date",
                            "0000"
                        )[:4]
                    ),

                    "rating": show.get(
                        "vote_average"
                    ),

                    "popularity": show.get(
                        "popularity"
                    )
                })

                time.sleep(0.1)

            except Exception:

                continue


# ============================================
# Module 32: Dataset Generation
# ============================================

print("Starting TMDB Dataset Generation...")

process_movies()

process_tv_shows()

df = pd.DataFrame(all_content)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/tmdb_content_v2.csv",
    index=False
)

print(
    f"Dataset Created Successfully! "
    f"Total Titles: {len(df)}"
)
