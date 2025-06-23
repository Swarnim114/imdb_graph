import time
import sys
import os
from pathlib import Path
from pyvis.network import Network

# Import modular components from the new package structure
from imdb_graph.utils.constants import NETWORK_OPTIONS
from imdb_graph.core.graph_utils import load_graph, prepare_similar_movies
from imdb_graph.visualization.network_builder import add_nodes_to_network, add_edges_to_network
from imdb_graph.visualization.html_enhancer import enhance_html_with_search as enhance_html

# Define default paths
DATA_DIR = Path(__file__).parent.parent.parent / "data"
JSON_PATH = DATA_DIR / "movie_graph.json"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "output"

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

def create_movie_network(movie_limit=250, output_filename=None):
    """Create a network visualization of movies.
    
    Args:
        movie_limit (int): Number of movies to include in the visualization
        output_filename (str, optional): Name of the output HTML file
        
    Returns:
        str: Path to the generated HTML file
    """
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if output_filename is None:
        output_filename = OUTPUT_DIR / f"{movie_limit}_movies.html"
    else:
        # Make sure the output_filename is a Path object
        output_filename = Path(output_filename)
        if not output_filename.is_absolute():
            output_filename = OUTPUT_DIR / output_filename
    
    print("Starting visualization process...")
    
    # Check if the graph data exists
    if not JSON_PATH.exists():
        print(f"Error: Graph data file not found at {JSON_PATH}")
        print("Please run the graph building script first.")
        return None
    
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
    
    # Convert Path to string if needed
    output_path_str = str(output_filename)
    net.show(output_path_str, notebook=False)
    
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