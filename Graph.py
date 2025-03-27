import networkx as nx

# --- Graph Class ---
class Graph:
    def __init__(self):
        self.G = nx.Graph()
        self.nodes = {}  # name: Node
        self.node_index = 0

    def generate_name(self):
        base = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        index = self.node_index
        suffix = "" if index < 26 else str(index // 26)
        name = base[index % 26] + suffix
        self.node_index += 1
        return name

    def add_node(self, x, y):
        name = self.generate_name()
        self.nodes[name] = Node(name, x, y)
        self.G.add_node(name)
        return name

    def delete_node(self, name):
        if name in self.nodes:
            self.G.remove_node(name)
            del self.nodes[name]

    def add_edge(self, node1, node2):
        if self.G.has_edge(node1,node2):
            self.G.remove_edge(node1,node2)
        else:
            self.G.add_edge(node1, node2)

    def add_all_edge(self, nodes):
        for i in range(len(nodes)-1):
            for j in range(i+1,len(nodes)):
                if not self.G.has_edge(nodes[i],nodes[j]):
                    self.G.add_edge(nodes[i],nodes[j])

    def remove_all_edges(self,nodes):
        for i in range(len(nodes)-1):
            for j in range(i+1,len(nodes)):
                if self.G.has_edge(nodes[i],nodes[j]):
                    self.G.remove_edge(nodes[i],nodes[j])


    def move_node(self, name, x, y):
        if name in self.nodes:
            self.nodes[name].move(x, y)

    def get_node_at(self, x, y, radius=0.1):
        closest_node = None
        min_dist_sq = radius * radius

        for name, node in self.nodes.items():
            dx = node.x - x
            dy = node.y - y
            dist_sq = dx * dx + dy * dy
            if dist_sq < min_dist_sq:
                min_dist_sq = dist_sq
                closest_node = name

        return closest_node

    def get_positions(self):
        return {name: node.position() for name, node in self.nodes.items()}

    def clear(self):
        self.G.clear()
        self.nodes.clear()
        self.node_index = 0

# --- Node Class ---
class Node:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def move(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return (self.x, self.y)