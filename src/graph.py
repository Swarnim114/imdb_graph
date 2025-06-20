import json
from collections import defaultdict

class MovieGraph:
    def __init__(self):
        self.adj_list = defaultdict(list)  # movie_id -> list of (neighbor_id, weight)
        self.nodes_data = {}  # movie_id -> movie dict

    def add_node(self, movie_id, movie_data):
        self.nodes_data[movie_id] = movie_data

    def add_edge(self, id1, id2, weight):
        self.adj_list[id1].append((id2, weight))
        self.adj_list[id2].append((id1, weight))  # undirected

    def get_neighbors(self, movie_id):
        return self.adj_list[movie_id]

    def get_node_data(self, movie_id):
        return self.nodes_data.get(movie_id, None)

    def get_all_nodes(self):
        return list(self.nodes_data.keys())

    def get_num_nodes(self):
        return len(self.nodes_data)

    def get_num_edges(self):
        return sum(len(neighs) for neighs in self.adj_list.values()) // 2

    def save_to_json(self, path):
        # Convert defaultdict to regular dict for JSON serialization
        adj_list = {str(k): v for k, v in self.adj_list.items()}
        nodes_data = {str(k): v for k, v in self.nodes_data.items()}
        with open(path, 'w') as f:
            json.dump({
                'adj_list': adj_list,
                'nodes_data': nodes_data
            }, f, indent=2)

    @staticmethod
    def load_from_json(path):
        with open(path, 'r') as f:
            data = json.load(f)
        g = MovieGraph()
        g.adj_list = defaultdict(list, {int(k): v for k, v in data['adj_list'].items()})
        g.nodes_data = {int(k): v for k, v in data['nodes_data'].items()}
        return g

def calculate_similarity_weight(m1, m2):
    score = 0
    # Genre: 3 points if at least one genre overlaps
    if set(m1['genres']) & set(m2['genres']):
        score += 3
    # Rating: 3 points if ratings within 0.5
    if m1['rating'] is not None and m2['rating'] is not None:
        if abs(m1['rating'] - m2['rating']) <= 0.5:
            score += 3
    # Director: 2 points if same director
    if m1['director'] and m2['director'] and m1['director'] == m2['director']:
        score += 2
    # Actors: 1 point if 2 or more actors overlap
    if len(set(m1['cast']) & set(m2['cast'])) >= 2:
        score += 1
    # Year: 1 point if years within 2
    if m1['year'] and m2['year'] and abs(m1['year'] - m2['year']) <= 2:
        score += 1
    return score
