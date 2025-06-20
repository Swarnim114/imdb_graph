import time
from pathlib import Path
from pyvis.network import Network

# Import modular components - use absolute imports for better compatibility
from src.constants import NETWORK_OPTIONS
from src.graph_utils import load_graph, prepare_similar_movies, JSON_PATH
from src.network_builder import add_nodes_to_network, add_edges_to_network
from src.html_enhancer import enhance_html_with_search as enhance_html

# These functions have been moved to other modules
# See:
# - graph_utils.py for load_graph and prepare_similar_movies
# - network_builder.py for create_movie_tooltip, add_nodes_to_network, and add_edges_to_network

def configure_network_options(net):
    """Configure the network visualization options.
    
    Args:
        net (Network): Pyvis Network object
        
    Returns:
        None
    """
    # Enable the physics buttons
    net.show_buttons(filter_=['physics'])
    
    # Set physics options and other network configurations using the constant
    net.set_options(NETWORK_OPTIONS)

# These functions are not needed anymore since we're using the modular approach
# def get_search_css():
#     """Get the CSS for the search functionality.
#     Deprecated: Now loaded from separate file.
#     Returns:
#         str: Empty string
#     """
#     return ""
# 
# def get_search_html():
#     """Get the HTML for the search functionality.
#     Deprecated: Now loaded from separate file.
#     Returns:
#         str: Empty string
#     """
#     return ""
# 
# def get_search_js():
#     """Get the JavaScript for the search functionality.
#     Deprecated: Now loaded from separate file.
#     Returns:
#         str: Empty string
#     """
#     return ""
# 
# # This function is not needed anymore
# def enhance_html_with_search(filename):
#     """Enhance the HTML file with search functionality.
#     Deprecated: Use html_enhancer.enhance_html_with_search instead.
#     """
#     print("Warning: Using deprecated enhance_html_with_search function in visualize.py.")
#     print("Please use the function from html_enhancer.py instead.")
#     enhance_html(filename)

def create_movie_network(movie_limit=250, output_filename=None):
    """Create a network visualization of movies.
    
    Args:
        movie_limit (int): Number of movies to include in the visualization
        output_filename (str, optional): Name of the output HTML file
        
    Returns:
        str: Path to the generated HTML file
    """
    if output_filename is None:
        output_filename = f"{movie_limit}_movies.html"
    
    print("Starting visualization process...")
    movie_graph = load_graph(JSON_PATH)
    
    # Create a Pyvis Network object
    print("Creating network object...")
    net = Network(
        notebook=False, 
        height="100vh", 
        width="100%", 
        bgcolor="#222222", 
        font_color="white", 
        cdn_resources='remote'
    )
    
    # Use specified number of movies for the graph
    nodes_data = movie_graph["nodes_data"][:movie_limit]
    adj_list = movie_graph["adj_list"][:movie_limit]
    
    # Prepare similarity data
    top_similar_movies = prepare_similar_movies(adj_list)
    
    # Add nodes and edges
    add_nodes_to_network(net, nodes_data, top_similar_movies, movie_limit)
    add_edges_to_network(net, adj_list, movie_limit)
    
    # Configure network options
    configure_network_options(net)
    
    # Generate the HTML file
    print(f"Generating HTML file: {output_filename}")
    start_time = time.time()
    net.show(output_filename, notebook=False)
    
    # Enhance the HTML with search functionality
    enhance_html(output_filename)
    
    print(f"HTML file generated in {time.time() - start_time:.2f} seconds")
    print(f"Done! Open {output_filename} in your browser to view the graph with search functionality.")
    
    return output_filename

def main():
    """Main function to run the visualization."""
    create_movie_network(movie_limit=250)

if __name__ == "__main__":
    main()