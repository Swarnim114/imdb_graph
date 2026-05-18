# Interview Notes: IMDB Movie Graph Visualization

Use this sheet as a 5–10 minute walkthrough of the project. It highlights the design decisions behind the features listed on the resume.

## 1) System overview (30–60 seconds)

- **Goal**: Visualize relationships between IMDB movies so users can explore clusters of similar films.
- **Pipeline**:
  1. Fetch and normalize movie metadata (genres, rating, director, cast, year).
  2. Compute similarity scores between movies.
  3. Build a graph (movies = nodes, similarity = weighted edges).
  4. Serialize graph to JSON.
  5. Render an interactive HTML graph with search, color-coding, and tooltips.

## 2) Core design decisions (2–3 minutes)

### Graph representation
- **Adjacency list** (`MovieGraph.adj_list`) because the similarity graph is sparse after applying a threshold.
- **Trade-off**: Adjacency list makes traversal fast and storage compact, but random edge lookup is slower than a matrix.

### Similarity scoring
Implemented in `imdb_graph/core/graph.py`:
- **Genres overlap** → +3
- **Rating within ±1.0** → +3
- **Same director** → +2
- **≥2 shared cast members** → +1
- **Year within ±5** → +2

Edges are created only when the **total score exceeds a threshold** (default: 6). This keeps the graph readable and reduces visual noise.

### Visualization stack
- **Python** for preprocessing and graph generation.
- **PyVis (vis.js under the hood)** for the interactive network layout and rendering.
- **Custom JS/CSS** for fast search, highlighting, and UI elements.

This split keeps heavy computation in Python while leveraging a browser-native graph engine for interactivity.

## 3) UX features from the resume (2–3 minutes)

### Fast search
- Implemented in `imdb_graph/static/js/search.js`.
- Uses the in-memory node dataset from the vis.js network for lookups.
- Search is instant because it avoids server calls and only scans the existing node labels.

### Genre-based coloring
- Colors come from `GENRE_COLORS` in `imdb_graph/utils/constants.py`.
- Each node is colored by its **primary genre** to surface clusters visually.

### Tooltips
- Built in `imdb_graph/visualization/network_builder.py`.
- Tooltip lists a movie’s genre plus the **top 5 most similar movies** (precomputed from the adjacency list).

## 4) Performance and scalability (1–2 minutes)

- **Precomputation**: Similarity scores and top neighbors are computed offline and stored in JSON.
- **Sparse thresholding**: Prevents dense graphs and keeps rendering interactive.
- **Size control**: `movie_limit` defaults to 250 to ensure smooth browser performance.

## 5) Trade-offs & extensions (1–2 minutes)

**Current trade-offs**
- Similarity is heuristic and weighted, not ML-based.
- O(N²) similarity calculation is acceptable for the top-N subset but would need optimization for full IMDB scale.

**Potential improvements**
- Use approximate nearest neighbors for scalable similarity.
- Add faceted filters (year ranges, rating sliders).
- Persist a search index for larger datasets.

