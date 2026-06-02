import requests
import pandas as pd

API_KEY = "b0fe98cc89a85072d43d4997080ec5f4"

all_content = []


def fetch_data(endpoint, content_type):

    for page in range(1, 11):

        url = (
            f"https://api.themoviedb.org/3/{endpoint}"
            f"?api_key={API_KEY}"
            f"&page={page}"
        )

        response = requests.get(url)

        data = response.json()

        for item in data.get("results", []):

            title = item.get("title") or item.get("name")

            all_content.append({
                "title": title,
                "type": content_type,
                "description": item.get("overview", ""),
                "release_date": (
                    item.get("release_date")
                    or item.get("first_air_date")
                ),
                "rating": item.get("vote_average"),
                "popularity": item.get("popularity")
            })


print("Fetching Popular Movies...")
fetch_data("movie/popular", "Movie")

print("Fetching Top Rated Movies...")
fetch_data("movie/top_rated", "Movie")

print("Fetching Popular TV Shows...")
fetch_data("tv/popular", "TV Show")

print("Fetching Top Rated TV Shows...")
fetch_data("tv/top_rated", "TV Show")

df = pd.DataFrame(all_content)

df.drop_duplicates(
    subset=["title"],
    inplace=True
)

df.to_csv(
    "data/tmdb_content.csv",
    index=False
)

print(
    f"Dataset Created Successfully! "
    f"Total Titles: {len(df)}"
)