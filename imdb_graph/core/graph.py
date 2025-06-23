import json

class MovieGraph:
    def __init__(self, num_nodes):
        # Initialize a 2D list with empty lists for each node
        self.adj_list = [[] for _ in range(num_nodes)]
        self.nodes_data = [None] * num_nodes

    def add_node(self, node_id, movie_data):
        # Store movie data for the node
        self.nodes_data[node_id] = movie_data

    def add_edge(self, id1, id2, weight):
        # Add an edge between id1 and id2 with the given weight
        self.adj_list[id1].append((id2, weight))
        self.adj_list[id2].append((id1, weight))  # Undirected graph

    def get_neighbors(self, node_id):
        # Return the neighbors of the given node
        return self.adj_list[node_id]

    def get_node_data(self, node_id):
        # Return the data of the given node
        return self.nodes_data[node_id]

    def get_all_nodes(self):
        # Return all nodes that have data
        return [i for i, data in enumerate(self.nodes_data) if data is not None]

    def get_num_nodes(self):
        # Return the number of nodes with data
        return len([data for data in self.nodes_data if data is not None])

    def get_num_edges(self):
        # Count the number of edges
        count = 0
        for neighbors in self.adj_list:
            count += len(neighbors)
        return count // 2  # Each edge is counted twice

    def save_to_json(self, path):
        # Convert adjacency list and node data to JSON format
        adj_list = []
        for neighbors in self.adj_list:
            adj_list.append(neighbors)

        with open(path, 'w') as f:
            json.dump({
                'adj_list': adj_list,
                'nodes_data': self.nodes_data
            }, f, indent=2)

    @staticmethod
    def load_from_json(path):
        # Load adjacency list and node data from JSON file
        with open(path, 'r') as f:
            data = json.load(f)

        graph = MovieGraph(len(data['nodes_data']))
        graph.adj_list = data['adj_list']
        graph.nodes_data = data['nodes_data']
        return graph

    def build_graph(self, movies, threshold=6):
        """
        Build the graph by adding edges between movies with similarity score > threshold.

        :param movies: List of movie data dictionaries.
        :param threshold: Minimum similarity score to create an edge.
        """
        # Add all movies as nodes
        for i, movie in enumerate(movies):
            self.add_node(i, movie)

        # Compare each pair of movies and add edges if similarity score > threshold
        for i in range(len(movies)):
            for j in range(i + 1, len(movies)):
                score = calculate_similarity_weight(movies[i], movies[j])
                if score > threshold:
                    self.add_edge(i, j, score)

def calculate_similarity_weight(m1, m2):
    score = 0
    if len(set(m1['genres']).intersection(set(m2['genres']))) > 0:
        score += 3
    if m1['rating'] is not None and m2['rating'] is not None:
        if abs(m1['rating'] - m2['rating']) <= 1.0:
            score += 3
    if m1['director'] == m2['director']:
        score += 2
    if len(set(m1['cast']).intersection(set(m2['cast']))) >= 2:
        score += 1
    if m1['year'] is not None and m2['year'] is not None:
        if abs(m1['year'] - m2['year']) <= 5:
            score += 2
    return score
