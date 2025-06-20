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

# Define the network visualization options as a constant
NETWORK_OPTIONS = '''{
  "physics": {
    "enabled": true,
    "hierarchicalRepulsion": {
      "centralGravity": 4,
      "avoidOverlap": null
    },
    "maxVelocity": 5,
    "minVelocity": 1,
    "solver": "hierarchicalRepulsion",
    "timestep": 0.5
  },
  "interaction": {
    "hover": true,
    "zoomView": true,
    "dragNodes": true,
    "navigationButtons": true,
    "keyboard": {
      "enabled": true,
      "speed": {
        "x": 10,
        "y": 10,
        "zoom": 0.02
      },
      "bindToWindow": true
    }
  },
  "search": true,
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
    "filter": ["physics"]
  },
  "manipulation": {
    "enabled": false
  }
}'''
