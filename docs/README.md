# IMDB Movie Graph Documentation

This directory contains documentation for the IMDB Movie Graph project.

## Contents

- `migration_plan.md`: Plan for migrating from the old structure to the new package structure
- `developer_guide.md`: Guide for developers who want to extend the project
- `original_readme.md`: The original README from before the restructuring

## Project Architecture

The IMDB Movie Graph project is structured as a Python package with several modules:

### Core Components

- **Graph Module**: Implements the graph data structure using an adjacency list
- **Visualization Module**: Creates interactive visualizations using PyVis
- **Data Module**: Handles fetching and processing movie data

### Data Flow

1. Movie data is fetched from an external source (TMDB API)
2. A graph is built with movies as nodes and similarity as edges
3. The graph is serialized to JSON for later use
4. The visualization module creates an interactive HTML file
5. Search functionality is added to the HTML

## Design Decisions

- **Adjacency List**: Used for the graph representation for its efficiency in storing sparse graphs
- **PyVis Library**: Used for visualization due to its interactive features and HTML output
- **Modular Structure**: Components are separated into modules for better maintainability
- **Package-based Organization**: The project follows Python package conventions for better distribution

## Future Development

See the `migration_plan.md` file for future development plans and enhancements.
