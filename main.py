#костыль
import numpy as np
np.int = int
np.float = float
np.bool = bool 
#

import networkx as nt
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
    
def main():
    graph = nt.Graph()
    graph = get_data_from_json("cntrs.json", graph)

    sub = get_largest_connected_subgraph(graph)
    #2
    utils.analyze_graph(sub)
    
    #3
    print("Chromatic number:", utils.chromatic_number(sub))

if __name__ == "__main__":
    main()