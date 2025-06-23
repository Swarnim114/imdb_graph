# IMDB Movie Graph Visualization

This project creates interactive graph visualizations of movie relationships based on IMDB data. Movies are connected based on similarity, and the visualization includes a powerful search feature.



https://github.com/user-attachments/assets/5d08796e-a7e5-432e-a41d-04919ce7d3d8



## Features

- Interactive graph visualization of top IMDB movies
- Movies colored by genre
- Force-directed layout that groups similar movies together
- Search functionality to quickly find movies
- Responsive UI with keyboard shortcuts
- Tooltips showing movie details and similar movies

## Project Structure

```text
imdb_graph/
├── data/
│   ├── movie_graph.json    # Movie graph data (nodes and adjacency list)
│   └── movies_data.json    # Raw movie data
├── lib/                    # External libraries
├── src/
│   ├── constants.py        # Constants and configuration values
│   ├── data_fetch.py       # Functions for fetching movie data
│   ├── graph.py            # Graph manipulation functions
│   ├── graph_utils.py      # Utility functions for graph data
│   ├── html_enhancer.py    # Functions to enhance HTML with search functionality
│   ├── main.py             # Main entry point
│   ├── network_builder.py  # Functions to build network visualizations
│   ├── static/             # Static resources for the visualization
│   │   ├── css/            # CSS styles
│   │   └── js/             # JavaScript files
│   ├── utils.py            # General utility functions
│   └── visualize.py        # Core visualization functions
├── templates/              # HTML templates for visualization
└── tests/                  # Test directory
```

## Usage

### Building the Movie Graph

To build the movie graph from raw data:

```bash
python -m src.main build
```

This process only needs to be done once to generate the graph data.

### Creating the Visualization

To create an interactive visualization of the movie graph:

```bash
# Create visualization with default 250 movies
python -m src.main visualize

# Create visualization with custom number of movies
python -m src.main visualize 100
```

This will generate an HTML file (e.g., `250_movies.html`) that you can open in any modern web browser.

### Using the Visualization

1. **Open** the generated HTML file in your browser
2. **Search** for movies using the search box in the top-left corner
3. **Navigate** the graph by dragging and zooming
4. **Explore** movie relationships by clicking on nodes
5. **Keyboard shortcuts**:
   - Press `/` to focus the search box
   - Press `Esc` to clear search and hide results

## Modular Design

The codebase has been organized into modular components:

- `constants.py`: Central location for configuration values
- `graph_utils.py`: Functions for loading and processing graph data
- `network_builder.py`: Functions for building network visualizations
- `html_enhancer.py`: Functions to enhance HTML with search functionality
- `static/`: Directory for static resources
- `visualize.py`: Main interface for creating visualizations

This modular structure makes the code more maintainable and easier to extend.

## Search Functionality

The search functionality allows users to quickly find movies in the graph:

1. The search box is located in the top-left corner of the visualization
2. Start typing to search for a movie by title
3. Results appear in real-time below the search box
4. Click on a result to highlight the movie in the graph and zoom to it
5. Use keyboard shortcuts (`/` to focus, `Esc` to clear) for faster navigation

The search interface is designed to be:

- Responsive and fast
- Visually integrated with the graph
- Accessible via keyboard shortcuts
- Clear and easy to use
