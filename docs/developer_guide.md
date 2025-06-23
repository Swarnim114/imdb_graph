# Developer Guide

This guide provides information on how to extend and contribute to the IMDB Movie Graph project.

## Setting Up Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/imdb_graph.git
   cd imdb_graph
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install in development mode:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

## Project Structure

The project is organized as a Python package with the following structure:

- `imdb_graph/core/`: Core graph data structures and algorithms
- `imdb_graph/utils/`: Utility functions and constants
- `imdb_graph/visualization/`: Visualization components
- `imdb_graph/data/`: Data fetching and processing
- `imdb_graph/static/`: Static resources (CSS, JS)

## Adding New Graph Algorithms

To add new graph algorithms:

1. Add your algorithm to an appropriate module in `imdb_graph/core/`
2. For complex algorithms, consider creating a new module
3. Update the main interface if necessary

Example for adding a shortest path algorithm:

```python
# imdb_graph/core/algorithms.py

def find_shortest_path(graph, start_node, end_node):
    """Find the shortest path between two nodes in the graph.
    
    Args:
        graph: The MovieGraph object
        start_node: Starting node ID
        end_node: Ending node ID
        
    Returns:
        list: List of nodes in the path, or empty list if no path exists
    """
    # Implementation of Dijkstra's or BFS algorithm
    # ...
    return path
```

## Improving Visualization

To enhance the visualization:

1. Modify the CSS in `imdb_graph/static/css/`
2. Update JavaScript in `imdb_graph/static/js/`
3. For major changes, consider updating the HTML template injection in `html_enhancer.py`

## Adding a New Feature

When adding a new feature:

1. Identify the appropriate module for your feature
2. Add necessary functions/classes
3. Update the main interface if needed
4. Add tests for your feature
5. Update documentation

## Testing

To run tests:

```bash
# Future implementation - add pytest
pytest
```

## Creating a Pull Request

1. Fork the repository
2. Create a branch for your feature
3. Make your changes
4. Run tests
5. Submit a pull request with a clear description of your changes
