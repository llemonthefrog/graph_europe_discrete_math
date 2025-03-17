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

def main():
    graph = nt.Graph()
    graph = get_data_from_json("cntrs.json", graph)

    sub = get_largest_connected_subgraph(graph)
    
    utils.analyze_graph(sub)
    
    print(len(graph.nodes), len(graph.edges))
    
    print("Chromatic number:", utils.chromatic_number(sub))

    print("Art. points:", utils.found_artic_points(graph))
    
    print("Bridges:", utils.found_bridges(graph))
    
    weight_graph = nt.Graph()
    weight_graph = get_data_with_weight_from_json("cntrs.json", weight_graph)
    
    sub_weight = get_largest_connected_subgraph(weight_graph)
    
    mst, _ = utils.kruskal_minimum_spanning_tree(sub_weight)
    
    print(utils.prufer_code(mst))

if __name__ == "__main__":
    main()