import json
import sys
import os
from pathlib import Path

# Import from the new package structure
from imdb_graph.core.graph import MovieGraph
from imdb_graph.utils.constants import DEFAULT_OUTPUT_DIR

THRESHOLD = 7  # Minimum similarity score to create an edge

# Define default data paths
DATA_DIR = Path(__file__).parent.parent / "data"
MOVIES_DATA_PATH = DATA_DIR / "movies_data.json"
MOVIE_GRAPH_PATH = DATA_DIR / "movie_graph.json"

# Load movie data
def load_movies(path=MOVIES_DATA_PATH):
    """Load movie data from JSON file.
    
    Args:
        path: Path to the JSON file containing movie data
        
    Returns:
        list: List of movie dictionaries
    """
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    """Build the movie graph from raw data and save it to JSON."""
    print("Loading movies...")
    
    # Ensure data directory exists
    os.makedirs(DATA_DIR, exist_ok=True)
    
    if not MOVIES_DATA_PATH.exists():
        print(f"Error: Movie data file not found at {MOVIES_DATA_PATH}")
        print("Please run the data fetch script first or provide the correct path.")
        return
    
    movies = load_movies(MOVIES_DATA_PATH)
    print(f"Loaded {len(movies)} movies.")

    # Initialize the graph with the number of movies
    graph = MovieGraph(len(movies))

    # Build the graph using the new method
    print("Building the graph (this may take a while)...")
    graph.build_graph(movies, threshold=THRESHOLD)

    print(f"Graph built: {graph.get_num_nodes()} nodes, {graph.get_num_edges()} edges.")

    # Print sample neighbors for the first 3 movies
    for movie in movies[:3]:
        neighbors = graph.get_neighbors(movie['id'])
        print(f"\nMovie: {movie['title']} ({movie['year']})")
        print("Neighbors:")
        for neighbor_id, weight in neighbors[:5]:
            neighbor = graph.get_node_data(neighbor_id)
            print(f"  - {neighbor['title']} (weight: {weight})")

    # Save the graph to JSON for later use
    graph.save_to_json(MOVIE_GRAPH_PATH)
    print(f"Graph saved to {MOVIE_GRAPH_PATH}")

def visualize_graph():
    """Run the visualization module to create an interactive graph."""
    try:
        from imdb_graph.visualization.visualize import create_movie_network
        
        # Default to 250 movies
        movie_limit = 250
        
        # Parse command line arguments if provided
        if len(sys.argv) > 2:
            try:
                movie_limit = int(sys.argv[2])
                print(f"Creating visualization with {movie_limit} movies...")
            except ValueError:
                print(f"Error: {sys.argv[2]} is not a valid number of movies.")
                print("Using default value of 250 movies.")
        
        # Create the visualization
        output_file = create_movie_network(movie_limit=movie_limit)
        print(f"\nVisualization created: {output_file}")
        print(f"Open this file in your web browser to explore the movie graph.")
    except ImportError as e:
        print(f"Error: Could not import visualization module: {e}")
        print("Make sure all dependencies are installed.")
    except Exception as e:
        print(f"Error creating visualization: {e}")

def _run_command():
    """Entry point for command-line usage."""
    command = "build"  # Default command
    
    # Check if a command was provided
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
    
    if command == "build":
        main()
    elif command == "visualize":
        visualize_graph()
    else:
        print("Invalid command. Available commands:")
        print("  build     - Build the movie graph from raw data")
        print("  visualize - Create a visualization of the movie graph")
        print("\nExample usage:")
        print("  python -m imdb_graph.main build")
        print("  python -m imdb_graph.main visualize")
        print("  python -m imdb_graph.main visualize 100  # Visualize with 100 movies")

if __name__ == "__main__":
    _run_command()
