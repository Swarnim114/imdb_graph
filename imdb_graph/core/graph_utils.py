import json
import time
from pathlib import Path

# Import from the package
from imdb_graph.utils.constants import DATA_DIR

# Define the path to the JSON file
JSON_PATH = DATA_DIR / "movie_graph.json"

def load_graph(json_path=JSON_PATH):
    """Load the movie graph data from a JSON file.
    
    Args:
        json_path (Path): Path to the JSON file containing graph data
        
    Returns:
        dict: The loaded graph data
    """
    print(f"Loading graph data from JSON file: {json_path}")
    start = time.time()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"JSON data loaded in {time.time() - start:.2f} seconds")
    return data

def prepare_similar_movies(adj_list):
    """Prepare a dictionary to store top similar movies for each movie.
    
    Args:
        adj_list (list): Adjacency list representation of the graph
        
    Returns:
        dict: Dictionary mapping movie index to list of top similar movies
    """
    top_similar_movies = {}
    for idx, neighbors in enumerate(adj_list):
        # Sort neighbors by weight in descending order
        sorted_neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)
        # Get top 5 or fewer similar movies
        top_5 = sorted_neighbors[:5]
        # Store the top 5 similar movies with their weights
        top_similar_movies[idx] = top_5
    return top_similar_movies
