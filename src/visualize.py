import json
from pathlib import Path
from pyvis.network import Network
import time

# Define the path to the JSON file
json_path = Path(__file__).parent.parent / "data" / "movie_graph.json"

# Genre color mapping
GENRE_COLORS = {
    'Action': '#FF5733',
    'Comedy': '#33FF57',
    'Drama': '#3357FF',
    'Fantasy': '#F333FF',
    'Horror': '#FF33A1',
    'Romance': '#FF33B5',
    'Thriller': '#33FFF5',
    'Science Fiction': '#FF8333',
    'Documentary': '#33FF8A',
    'Animation': '#FF3385',
    'Mystery': '#B533FF',
    'Western': '#FF33D4',
    'Crime': '#33FFD4',
    'Family': '#FF33A8',
    'Adventure': '#33FF57',
    'Biography': '#FF33C1',
    'History': '#FF5733',
    'Musical': '#FF33F0',
    'Sport': '#33FF57',
    'War': '#FF3333',
    'Film Noir': '#B533FF',
    'Short Film': '#FF33D4',
    'News': '#33FFD4',
    'Reality-TV': '#FF33A8',
    'Talk-Show': '#33FF57',
    'Game-Show': '#FF5733',
    'Variety': '#FF33F0',
    'Adult': '#FF33C1',
    'N/A': '#808080'
}
DEFAULT_COLOR = '#1f78b4'

# Load the JSON data
def load_graph():
    print("Loading graph data from JSON file...")
    start = time.time()
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"JSON data loaded in {time.time() - start:.2f} seconds")
    return data

print("Starting visualization process...")
movie_graph = load_graph()

# Create a Pyvis Network object
print("Creating network object...")
net = Network(notebook=False, height="100vh", width="100%", bgcolor="#222222", font_color="white", cdn_resources='remote')

# Use all 1000 movies for the graph
nodes_data = movie_graph["nodes_data"][:1000]
adj_list = movie_graph["adj_list"][:1000]
total_nodes = len(nodes_data)
print(f"Processing {total_nodes} nodes...")

# Add nodes with color based on primary genre
start_time = time.time()
for idx, movie in enumerate(nodes_data):
    label = movie.get("title", f"Movie {idx+1}")
    genres = movie.get("genres", [])
    primary_genre = genres[0] if genres else 'N/A'
    color = GENRE_COLORS.get(primary_genre, DEFAULT_COLOR)
    tooltip = f"<b>{label}</b><br>Genre: {primary_genre}"
    net.add_node(idx, label=label, title=tooltip, color=color, size=15)
    
    if (idx + 1) % 100 == 0:
        print(f"Added {idx + 1}/{total_nodes} nodes ({(idx + 1)/total_nodes*100:.1f}%)...")

print(f"All nodes added in {time.time() - start_time:.2f} seconds")

# Add edges (only between the first 1000 nodes)
print("Adding edges...")
edge_count = 0
start_time = time.time()
for idx, neighbors in enumerate(adj_list):
    for neighbor in neighbors:
        neighbor_id = neighbor[0]
        weight = neighbor[1]
        if neighbor_id < 1000:  # Only connect within the first 1000 nodes
            edge_width = weight / 20
            net.add_edge(idx, neighbor_id, width=edge_width, title=f"Similarity: {weight:.2f}")
            edge_count += 1
    
    if (idx + 1) % 100 == 0:
        print(f"Processed edges for {idx + 1}/{total_nodes} nodes, added {edge_count} edges so far...")

print(f"All edges added in {time.time() - start_time:.2f} seconds. Total edges: {edge_count}")

# Set custom physics options for the network
print("Setting network options...")

# **DOUBLE-CHECKED FOR ALL DOUBLE QUOTES AROUND KEYS**
net.set_options('''{
  "physics": {
    "enabled": true,
    "forceAtlas2Based": {
      "gravitationalConstant": -50,
      "centralGravity": 0.005,
      "springLength": 50,
      "springConstant": 0.05,
      "avoidOverlap": 0.5
    },
    "maxVelocity": 5,
    "minVelocity": 0.1,
    "solver": "forceAtlas2Based",
    "stabilization": {
      "enabled": true,
      "iterations": 1000,
      "updateInterval": 25,
      "fit": true
    }
  },
  "interaction": {
    "hover": true,
    "zoomView": true,
    "dragNodes": true,
    "navigationButtons": true
  },
  "nodes": {
    "font": {"size": 14, "color": "white", "strokeWidth": 0, "strokeColor": "#333333"},
    "shape": "dot"
  },
  "edges": {
    "color": {"inherit": "from"},
    "smooth": {"enabled": true, "type": "continuous", "roundness": 0.5}
  },
  "configure": {
    "enabled": true,
    "filter": ["physics", "nodes", "edges", "interaction"]
  }
}''')

# Show the network (generates and opens an HTML file)
print("Generating HTML file...")
start_time = time.time()
net.show("1000_movies.html", notebook=False)
print(f"HTML file generated in {time.time() - start_time:.2f} seconds")
print("Done! Open 1000_movies.html in your browser to view the graph.")