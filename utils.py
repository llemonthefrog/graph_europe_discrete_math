from collections import deque
import networkx as nt

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

def ddfs(graph, start, visited):
    visited.add(start)
    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            ddfs(graph, neighbor, visited)


def count_connected_components(graph):
    visited = set()
    connected_components = 0

    for vertex in graph.nodes():
        if vertex not in visited:
            ddfs(graph, vertex, visited)
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
    
    print("Degrees", get_degrees(graph))
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
    return solve_coloring(0, 0, {}) - 1

def found_artic_points(graph):
    vertexes = []
    
    comp_count: int = count_connected_components(graph)
    for v in list(graph.nodes):
        subgraph = graph.copy()
        subgraph.remove_node(v)
        
        sub_comp_count: int = count_connected_components(subgraph)
        if(sub_comp_count > comp_count):
            vertexes.append(v)
            
    return vertexes
        
def found_bridges(graph):
    bridges = []
    
    comp_count: int = count_connected_components(graph)
    for u, v in list(graph.edges):
        subgraph = graph.copy()
        subgraph.remove_edge(u, v)
        
        sub_comp_count: int = count_connected_components(subgraph)
        if(sub_comp_count > comp_count):
            bridges.append([u, v])
            
    return bridges


def kruskal_minimum_spanning_tree(graph):
    edges = sorted(graph.edges(data=True), key=lambda x: x[2]['weight'])
    
    parent = {}
    rank = {}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1
    
    for node in graph.nodes:
        parent[node] = node
        rank[node] = 0
    
    mst_graph = nt.Graph()
    mst_weight = 0
    
    for edge in edges:
        u, v, weight = edge[0], edge[1], edge[2]['weight']
        if find(u) != find(v):
            union(u, v)
            mst_graph.add_edge(u, v, weight=weight)
            mst_weight += weight
    
    return mst_graph, mst_weight

def prufer_code(tree):
    graph = tree.copy()
    
    prufer = []
    
    while len(graph.nodes) > 2:
        leaf = min([node for node in graph.nodes if graph.degree[node] == 1])
        
        neighbor = list(graph.neighbors(leaf))[0]
        prufer.append(neighbor)

        graph.remove_node(leaf)
    
    return prufer

def is_eulerian(graph):
    return nt.is_connected(graph) and all(degree % 2 == 0 for _, degree in graph.degree())

def maximal_eulerian_subgraph(graph):
    subgraph = graph.copy()

    while not is_eulerian(subgraph):
        odd_degree_nodes = [node for node, degree in subgraph.degree() if degree % 2 != 0]
        
        if len(odd_degree_nodes) <= 1:
            break

        edge_removed = False
        for node in odd_degree_nodes:
            for neighbor in list(subgraph.neighbors(node)):
                subgraph.remove_edge(node, neighbor)
                
                if nt.is_connected(subgraph):
                    edge_removed = True
                    break
                else:
                    subgraph.add_edge(node, neighbor)
            
            if edge_removed:
                break
        
        if not edge_removed:
            break
    
    return subgraph

def graph_to_binary_edges(graph):
    mapping = {node: idx for idx, node in enumerate(graph.nodes())}

    binary_representation = ""
    for edge in graph.edges():
        node1 = mapping[edge[0]]  
        node2 = mapping[edge[1]]
        
        binary_representation += format(node1, '08b') + format(node2, '08b')
    
    return binary_representation