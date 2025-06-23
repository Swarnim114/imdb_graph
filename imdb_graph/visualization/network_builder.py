import time
from imdb_graph.utils.constants import GENRE_COLORS, DEFAULT_COLOR

def create_movie_tooltip(movie, idx, top_similar_movies, nodes_data):
    """Create a tooltip for a movie node.
    
    Args:
        movie (dict): Movie data
        idx (int): Movie index
        top_similar_movies (dict): Dictionary of top similar movies
        nodes_data (list): List of all movie data
        
    Returns:
        str: Tooltip text
    """
    label = movie.get("title", f"Movie {idx+1}")
    genres = movie.get("genres", [])
    primary_genre = genres[0] if genres else 'N/A'
    
    # Create a plain text tooltip since HTML formatting isn't working correctly
    tooltip = f"{label}\nGenre: {primary_genre}\n\nTop Similar Movies:"
    
    # Add top 5 similar movies to the tooltip with plain text formatting
    if idx in top_similar_movies and top_similar_movies[idx]:
        # Explicitly show all similar movies (up to 5)
        similar_count = min(5, len(top_similar_movies[idx]))
        for i in range(similar_count):
            neighbor_id, weight = top_similar_movies[idx][i]
            if neighbor_id < len(nodes_data):  # Ensure neighbor_id is valid
                similar_movie = nodes_data[neighbor_id].get("title", f"Movie {neighbor_id+1}")
                # Use plain text formatting with newlines instead of HTML
                tooltip += f"\n{i+1}. {similar_movie} ({weight:.2f})"
    else:
        tooltip += "\nNo similar movies found"
    
    return tooltip

def add_nodes_to_network(net, nodes_data, top_similar_movies, limit=None):
    """Add movie nodes to the network.
    
    Args:
        net (Network): Pyvis Network object
        nodes_data (list): List of movie data
        top_similar_movies (dict): Dictionary of top similar movies
        limit (int, optional): Limit the number of nodes to add
        
    Returns:
        None
    """
    nodes_to_use = nodes_data[:limit] if limit else nodes_data
    total_nodes = len(nodes_to_use)
    print(f"Processing {total_nodes} nodes...")
    
    start_time = time.time()
    for idx, movie in enumerate(nodes_to_use):
        label = movie.get("title", f"Movie {idx+1}")
        genres = movie.get("genres", [])
        primary_genre = genres[0] if genres else 'N/A'
        color = GENRE_COLORS.get(primary_genre, DEFAULT_COLOR)
        
        tooltip = create_movie_tooltip(movie, idx, top_similar_movies, nodes_data)
        
        net.add_node(idx, label=label, title=tooltip, color=color, size=15)
        
        if (idx + 1) % 100 == 0:
            print(f"Added {idx + 1}/{total_nodes} nodes ({(idx + 1)/total_nodes*100:.1f}%)...")
    
    print(f"All nodes added in {time.time() - start_time:.2f} seconds")

def add_edges_to_network(net, adj_list, limit=None):
    """Add edges to the network.
    
    Args:
        net (Network): Pyvis Network object
        adj_list (list): Adjacency list representation of the graph
        limit (int, optional): Limit connections to nodes within this limit
        
    Returns:
        int: Number of edges added
    """
    edges_limit = limit if limit else len(adj_list)
    total_nodes = min(len(adj_list), edges_limit)
    print("Adding edges...")
    edge_count = 0
    start_time = time.time()
    
    for idx, neighbors in enumerate(adj_list[:edges_limit]):
        for neighbor in neighbors:
            neighbor_id = neighbor[0]
            weight = neighbor[1]
            if neighbor_id < edges_limit:  # Only connect within the limit
                edge_width = weight / 20
                net.add_edge(idx, neighbor_id, width=edge_width, title=f"Similarity: {weight:.2f}")
                edge_count += 1
        
        if (idx + 1) % 100 == 0:
            print(f"Processed edges for {idx + 1}/{total_nodes} nodes, added {edge_count} edges so far...")
    
    print(f"All edges added in {time.time() - start_time:.2f} seconds. Total edges: {edge_count}")
    return edge_count
