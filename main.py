#костыль
import numpy as np
np.int = int
np.float = float
np.bool = bool 
#

import networkx as nt
import matplotlib.pyplot as plt
import json

import utils

def visualize_graph_spring(graph):
    import matplotlib.pyplot as plt
    import networkx as nt

    plt.figure(figsize=(12, 8))
    
    # spring_layout с оптимизированными параметрами
    pos = nt.spring_layout(graph,
                          k=1,  # Оптимальное расстояние между узлами
                          iterations=50,  # Количество итераций для оптимизации
                          scale=2)  # Масштаб графа
    
    # Визуализация узлов и рёбер
    nt.draw(graph,
            pos,
            with_labels=True,
            node_color='lightblue',
            node_size=500,
            font_size=10,
            font_weight='bold',
            edge_color='gray',
            width=1)

    # Добавим веса рёбер
    edge_labels = nt.get_edge_attributes(graph, 'weight')  # Получение атрибутов 'weight'
    nt.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9)

    plt.title("Graph Visualization (Spring Layout)")
    plt.axis('off')
    plt.tight_layout()
    
    return plt

def get_largest_connected_subgraph(graph):
    connected_components = nt.connected_components(graph)

    largest_component = max(connected_components, key=len)
    
    largest_subgraph = graph.subgraph(largest_component).copy()
    
    return largest_subgraph

def get_data_from_json(name: str, graph):
    with open(name, "r") as data:
        d = json.load(data) 

        for country in d["vctr"]:
            source = country["name"] 
            graph.add_node(source)
                
            for edge in country["edges"]:
                target = edge["name"]
                graph.add_edge(source, target) 
        
    return graph

def get_data_with_weight_from_json(name: str, graph):
    with open(name, "r") as data:
        d = json.load(data) 

        for country in d["vctr"]:
            source = country["name"] 
            graph.add_node(source)
                
            for edge in country["edges"]:
                target = edge["name"]
                weight = edge["h"]
                graph.add_edge(source, target, weight=weight) 
        
    return graph

def visualize_graph_min_edge_crossing(graph):
    """
    Визуализирует граф с минимальными пересечениями рёбер.
    
    :param graph: Граф NetworkX.
    """
    # Проверяем, является ли граф планарным
        # Если граф не планарный, используем spring_layout (энергетический алгоритм)
    pos = nt.spring_layout(graph, seed=42)  # seed для воспроизводимости

    # Визуализация графа с использованием найденных позиций
    plt.figure(figsize=(10, 8))
    nt.draw(graph, pos, with_labels=True, node_color="skyblue", node_size=500, edge_color="gray", font_size=10)
    plt.title("Визуализация графа с минимальными пересечениями рёбер")
    plt.show()
    
def main():
    graph = nt.Graph()
    graph = get_data_from_json("cntrs.json", graph)

    sub = get_largest_connected_subgraph(graph)
    
    #2
    utils.analyze_graph(sub)
    
    print(len(graph.nodes), len(graph.edges))
    
    #3
    print("Chromatic number:", utils.chromatic_number(sub))
    
    #5
    #visualize_graph_min_edge_crossing(utils.maximal_eulerian_subgraph(sub))
    
    #visualize_graph_min_edge_crossing(utils.find_max_hamiltonian_subgraph(sub))
    
    #g = utils.find_max_hamiltonian_subgraph(sub)
    
    #visualize_graph_spring(g).show()
    
    #7
    print("Art. points:", utils.found_artic_points(graph))
    
    #8
    print("Bridges:", utils.found_bridges(graph))
    
    #9
    weight_graph = nt.Graph()
    weight_graph = get_data_with_weight_from_json("cntrs.json", weight_graph)
    
    sub_weight = get_largest_connected_subgraph(weight_graph)
    
    mst, _ = utils.kruskal_minimum_spanning_tree(sub_weight)
    
    visualize_graph_spring(mst).show()
    
    
    #10
    print(utils.prufer_code(mst))

if __name__ == "__main__":
    main()