from Graph import Graph

# --- Coloring Logic Class ---
class ColoringLogic:
    def k_color(self, graph: Graph, k):
        def is_valid(node, color, coloring):
            for neighbor in graph.G.neighbors(node):
                if coloring.get(neighbor) == color:
                    return False
            return True

        def backtrack(index, coloring):
            if index == len(nodes):
                #print(coloring)
                return coloring
            node = nodes[index]
            for color in range(k):
                if is_valid(node, color, coloring):
                    coloring[node] = color
                    result = backtrack(index + 1, coloring.copy())
                    if result:
                        return result
            return None

        nodes = list(graph.G.nodes)
        return backtrack(0, {})