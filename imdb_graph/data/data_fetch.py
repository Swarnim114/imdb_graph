import requests
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '../.env'))
API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
MOVIE_COUNT = 1000  # Fetch top 10 for testing
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "../data/movies_data.json")

def get_movie_ids(pages=1):
    ids = []
    for page in range(1, pages + 1):
        url = (
            f"{BASE_URL}/discover/movie"
            f"?api_key={API_KEY}"
            f"&page={page}"
            f"&sort_by=vote_average.desc"
            f"&vote_count.gte=1000"
        )
        resp = requests.get(url)
        if resp.status_code != 200:
            print(f"Error fetching page {page}: {resp.status_code}")
            continue
        data = resp.json()
        ids += [m["id"] for m in data.get("results", [])]
        time.sleep(0.2)  
    return ids[:MOVIE_COUNT]  # Only return the top N ids

def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&append_to_response=credits"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    # Extract director
    director = ""
    for crew in data.get("credits", {}).get("crew", []):
        if crew["job"] == "Director":
            director = crew["name"]
            break
    # Extract top 5 cast
    cast = [c["name"] for c in data.get("credits", {}).get("cast", [])[:5]]
    return {
        "id": movie_id,
        "title": data.get("title"),
        "year": int(data.get("release_date", "0000-00-00")[:4]) if data.get("release_date") else None,
        "rating": data.get("vote_average"),
        "genres": [g["name"] for g in data.get("genres", [])],
        "director": director,
        "cast": cast,
    }

def main():
    print("Fetching top-rated movie IDs...")
    ids = get_movie_ids(pages=50)  # 50 pages x 20 movies per page = 1000 movies
    print(f"Found {len(ids)} movie IDs.")
    movies = []
    for i, movie_id in enumerate(ids):
        details = get_movie_details(movie_id)
        if details:
            movies.append(details)
        print(f"Fetched {i+1}/{len(ids)}", end="\r")
        time.sleep(0.2)
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(movies, f, indent=2)
    print(f"\nSaved {len(movies)} movies to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
