"""
Core module for the IMDB Movie Graph package.
Contains the main graph implementation and utilities.
"""

from .graph import MovieGraph
from .graph_utils import load_graph, prepare_similar_movies

__all__ = ['MovieGraph', 'load_graph', 'prepare_similar_movies']
