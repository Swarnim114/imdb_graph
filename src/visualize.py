import streamlit as st
from pyvis.network import Network
import networkx as nx
import tempfile
import os
from graph import MovieGraph

st.title("Movie Constellation Map")

# Load the saved graph
try:
    st.info("Loading graph from data/movie_graph.json...")
    graph = MovieGraph.load_from_json("data/movie_graph.json")
    st.success(f"Loaded graph with {graph.get_num_nodes()} nodes and {graph.get_num_edges()} edges")
except Exception as e:
    st.error(f"Error loading graph: {str(e)}")
    st.stop()

# Sidebar for filtering
st.sidebar.title("Visualization Options")
num_movies = st.sidebar.slider("Number of movies to show", 10, 100, 20)
min_weight = st.sidebar.slider("Minimum similarity score", 1, 10, 3)

# Build NetworkX graph from MovieGraph (with limits)
st.info("Building network visualization...")
G = nx.Graph()

# Get top N movies by number of connections
movie_connections = {movie_id: len(neighbors) for movie_id, neighbors in graph.adj_list.items()}
top_movies = sorted(movie_connections.items(), key=lambda x: x[1], reverse=True)[:num_movies]
top_movie_ids = [movie_id for movie_id, _ in top_movies]

# Add nodes for top movies
for movie_id in top_movie_ids:
    movie_data = graph.get_node_data(movie_id)
    G.add_node(movie_id, label=movie_data["title"])
    
# Add edges between these movies
for movie_id in top_movie_ids:
    neighbors = graph.get_neighbors(movie_id)
    for neighbor_id, weight in neighbors:
        if neighbor_id in top_movie_ids and weight >= min_weight:
            G.add_edge(movie_id, neighbor_id, weight=weight)

st.success(f"NetworkX graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

# Pyvis network with stabilization
net = Network(
    height="700px",
    width="100%",
    bgcolor="#222222",
    font_color="white",
    directed=False
)

# Configure physics for stability
net.set_options("""
{
  "physics": {
    "stabilization": {
      "enabled": true,
      "iterations": 100,
      "updateInterval": 100,
      "fit": true
    },
    "barnesHut": {
      "gravitationalConstant": -10000,
      "springConstant": 0.01,
      "springLength": 200,
      "centralGravity": 0.1,
      "damping": 0.95
    }
  },
  "edges": {
    "smooth": {
      "type": "continuous",
      "forceDirection": "none"
    }
  }
}
""")

net.from_nx(G)

# Configure nodes and edges
for node in net.nodes:
    movie_data = graph.get_node_data(int(node["id"]))
    node["title"] = f"{movie_data['title']} ({movie_data['year']})\nRating: {movie_data['rating']}"
    node["size"] = 10  # Smaller fixed size
    node["color"] = "#97c2fc"
    node["font"] = {"size": 12}  # Smaller font
    
for edge in net.edges:
    edge["color"] = {"color": "#cccccc", "opacity": 0.2}  # More subtle edges
    src = edge["from"]
    dst = edge["to"]
    try:
        weight = G[src][dst].get("weight", 1)
    except:
        weight = 1
    edge["width"] = weight / 2  # Thinner edges
    edge["title"] = f"Similarity: {weight}"

# Generate and display HTML
st.info("Generating visualization...")
with tempfile.TemporaryDirectory() as tmpdirname:
    html_path = os.path.join(tmpdirname, "graph.html")
    net.write_html(html_path)
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=750, scrolling=True)

st.write("Click a node to highlight its neighbors. Hover over nodes to see movie details.")
