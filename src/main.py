import json
from graph import MovieGraph

THRESHOLD = 7  # Minimum similarity score to create an edge

# Load movie data
def load_movies(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    print("Loading movies...")
    movies = load_movies("data/movies_data.json")
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
    graph.save_to_json("data/movie_graph.json")

if __name__ == "__main__":
    main()
