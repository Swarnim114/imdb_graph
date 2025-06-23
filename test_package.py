#!/usr/bin/env python3
"""
Test script to verify the IMDB Graph package functionality.
This script builds a small graph and creates a visualization.
"""

import os
import sys
from pathlib import Path
import time

# Import the package modules
from imdb_graph.core.graph import MovieGraph
from imdb_graph.visualization.visualize import create_movie_network
from imdb_graph.utils.constants import DATA_DIR, OUTPUT_DIR

def test_graph_build():
    """Test building a small movie graph."""
    print("Testing graph building...")
    
    # Create test movie data
    test_movies = [
        {
            "id": 0,
            "title": "Test Movie 1",
            "year": 2020,
            "genres": ["Action", "Thriller"],
            "director": "Test Director",
            "cast": ["Actor 1", "Actor 2"],
            "rating": 8.5
        },
        {
            "id": 1,
            "title": "Test Movie 2",
            "year": 2021,
            "genres": ["Comedy"],
            "director": "Test Director 2",
            "cast": ["Actor 3", "Actor 4"],
            "rating": 7.5
        },
        {
            "id": 2,
            "title": "Test Movie 3",
            "year": 2019,
            "genres": ["Drama", "Action"],
            "director": "Test Director 3",
            "cast": ["Actor 1", "Actor 5"],
            "rating": 9.0
        }
    ]
    
    # Create a graph
    graph = MovieGraph(len(test_movies))
    
    # Add nodes and edges
    for i, movie in enumerate(test_movies):
        graph.add_node(i, movie)
    
    # Add some edges
    graph.add_edge(0, 1, 6.5)  # Test Movie 1 -> Test Movie 2
    graph.add_edge(0, 2, 8.0)  # Test Movie 1 -> Test Movie 3
    
    # Test graph properties
    assert graph.get_num_nodes() == 3, "Graph should have 3 nodes"
    assert graph.get_num_edges() == 2, "Graph should have 2 edges"
    
    # Test neighbors
    neighbors_0 = graph.get_neighbors(0)
    assert len(neighbors_0) == 2, "Node 0 should have 2 neighbors"
    
    # Check if the neighbors are correct
    neighbor_ids = [n[0] for n in neighbors_0]
    assert 1 in neighbor_ids, "Node 1 should be a neighbor of Node 0"
    assert 2 in neighbor_ids, "Node 2 should be a neighbor of Node 0"
    
    print("✓ Graph building test passed!")
    return graph

def test_visualization(graph):
    """Test creating a visualization from the graph."""
    print("Testing visualization...")
    
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Save graph to JSON for visualization
    test_graph_path = DATA_DIR / "test_graph.json"
    os.makedirs(DATA_DIR, exist_ok=True)
    graph.save_to_json(test_graph_path)
    
    # Create a visualization
    start_time = time.time()
    output_file = create_movie_network(movie_limit=3, output_filename=OUTPUT_DIR / "test_visualization.html")
    print(f"Visualization created in {time.time() - start_time:.2f} seconds")
    
    # Check that the output file exists
    assert output_file.exists(), "Output file should exist"
    
    print("✓ Visualization test passed!")
    return output_file

def main():
    """Run all tests."""
    print("Running IMDB Graph package tests...")
    
    try:
        # Test graph building
        graph = test_graph_build()
        
        # Test visualization
        output_file = test_visualization(graph)
        
        print("\nAll tests passed successfully!")
        print(f"Visualization created at: {output_file}")
        
    except AssertionError as e:
        print(f"Test failed: {e}")
        return 1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
