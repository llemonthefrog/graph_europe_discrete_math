from collections import deque

def get_degrees(graph):
    degrees = []

    for node in graph.nodes:
        degree = 0
        for _ in graph.neighbors(node):
            degree += 1
        degrees.append(degree)

    return (min(degrees), max(degrees))

def get_distance(graph, vertex):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[vertex] = 0
    
    que = deque([vertex])

    while que:
        vert = que.popleft()
        for neighbor in graph.neighbors(vert):
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[vert] + 1
                que.append(neighbor)
    
    return distances

def dfs(graph, start, visited):
    visited.add(start)
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)


def count_connected_components(graph):
    visited = set()
    connected_components = 0

    for vertex in graph.nodes():
        if vertex not in visited:
            dfs(graph, vertex, visited)
            connected_components += 1

    return connected_components

def ecs(graph):
    ecscen = {}
    for node in graph.nodes():
        dist = get_distance(graph, node)
        finite_distances = [d for d in dist.values() if d != float('inf')]
        if finite_distances:
            ecscen[node] = max(finite_distances)
        else:
             ecscen[node] = float('inf')
    return ecscen

def get_radius(ecs):
    finite_eccentricities = [ecc for ecc in ecs.values() if ecc != float('inf')]
    return min(finite_eccentricities) if finite_eccentricities else float('inf')

def get_diameter(ecs):
    finite_eccentricities = [ecc for ecc in ecs.values() if ecc != float('inf')]
    return max(finite_eccentricities) if finite_eccentricities else float('inf')
   
def get_centers(component, eccentricities, radius):
    return [node for node in component if eccentricities[node] == radius]

def calculate_cyclomatic_number(graph):
    num_nodes = len(graph.nodes())
    num_edges = len(graph.edges())
    num_components = count_connected_components(graph)
    
    return num_edges - num_nodes + num_components

def analyze_graph(graph):
    eccentricities = ecs(graph)
       
    radius = get_radius(eccentricities)
       
    diameter = get_diameter(eccentricities)
       
    centers = get_centers(graph, eccentricities, radius)

    cyclomatic_number = calculate_cyclomatic_number(graph)
       
    print("Radius:", radius)
    print("Diameter:", diameter)
    print("Centers:", centers)
    print("Cyclomatic Number:", cyclomatic_number)
    
    
def chromatic_number(graph):
    def can_color(node, color, color_map):
        for neighbor in graph.neighbors(node):
            if color_map.get(neighbor) == color:
                return False
        return True

    def solve_coloring(node_index, colors_used, color_map):
        if node_index == len(nodes):
            return colors_used

        node = nodes[node_index]

        for color in range(colors_used + 1):
            if can_color(node, color, color_map):
                color_map[node] = color
                result = solve_coloring(node_index + 1, max(colors_used, color + 1), color_map)
                if result != -1:
                    return result
                del color_map[node] 

        return -1 

    nodes = list(graph.nodes)
    return solve_coloring(0, 0, {})
