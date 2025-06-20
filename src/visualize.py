import random
import streamlit as st
from pyvis.network import Network
import networkx as nx
import tempfile
import os
from graph import MovieGraph

# Configure page layout
st.set_page_config(layout='wide')
st.title('Movie Constellation Map')

# Define genre colors and default color
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
DEFAULT_COLOR = '#FFFFFF'

# Try to load and build the graph
try:
    # Load saved graph data
    graph = MovieGraph.load_from_json('data/movie_graph.json')
    G = nx.Graph()

    # Select 100 random movies
    all_movies = graph.get_all_nodes()
    random_movies = random.sample(all_movies, min(100, len(all_movies)))

    # Add nodes
    for mid in random_movies:
        md = graph.get_node_data(mid)
        G.add_node(mid, title=md.get('title', str(mid)))

    # Add edges between the selected movies
    for mid in random_movies:
        for nbr, wt in graph.get_neighbors(mid):
            if nbr in random_movies:
                G.add_edge(mid, nbr, weight=wt)

    # Create pyvis network
    net = Network(
        height='800px', width='100%', bgcolor='#111111', font_color='white', cdn_resources='remote'
    )

    # Enable physics for better layout
    net.toggle_physics(True)

    # Add nodes with fixed positions and genre colors
    for node in G.nodes():
        attrs = G.nodes[node]
        movie_data = graph.get_node_data(node)
        title = movie_data.get('title', str(node))
        primary = movie_data.get('genres', [None])[0]
        color = GENRE_COLORS.get(primary, DEFAULT_COLOR)

        # Add a tooltip with the 5 most similar movies
        neighbors = graph.get_neighbors(node)
        neighbors = sorted(neighbors, key=lambda x: x[1], reverse=True)[:5]  # Top 5 neighbors by weight
        tooltip = f"<b>{title}</b><br>Most Similar Movies:<br>"
        for neighbor_id, weight in neighbors:
            neighbor_data = graph.get_node_data(neighbor_id)
            tooltip += f"- {neighbor_data.get('title', 'Unknown')} (Similarity: {weight})<br>"

        net.add_node(
            node, 
            label=title, 
            title=tooltip,  # Tooltip with similar movies
            color=color, 
            size=20  # Increase node size for better visibility
        )

    # Add edges with weight-based width
    for u, v, data in G.edges(data=True):
        w = data['weight']
        net.add_edge(u, v, width=w/5, title=f"Similarity: {w}/10")

    # Generate and display HTML
    with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmp:
        net.save_graph(tmp.name)
        html = open(tmp.name, 'r', encoding='utf-8').read()
    st.components.v1.html(html, height=820, scrolling=True)
    os.remove(tmp.name)

except Exception as e:
    st.error(f"Error generating graph: {e}")
