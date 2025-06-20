import json
from graph import MovieGraph, calculate_similarity_weight

THRESHOLD = 3  # Minimum similarity score to create an edge

# Load movie data
def load_movies(path):
    with open(path, 'r') as f:
        return json.load(f)

def main():
    print("Loading movies...")
    movies = load_movies("data/movies_data.json")
    print(f"Loaded {len(movies)} movies.")
    graph = MovieGraph()
    # Add nodes
    for movie in movies:
        graph.add_node(movie['id'], movie)
    # Add edges
    n = len(movies)
    print("Building edges (this may take a while)...")
    for i in range(n):
        for j in range(i+1, n):
            w = calculate_similarity_weight(movies[i], movies[j])
            if w >= THRESHOLD:
                graph.add_edge(movies[i]['id'], movies[j]['id'], w)
        if (i+1) % 100 == 0:
            print(f"Processed {i+1}/{n} movies")
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
