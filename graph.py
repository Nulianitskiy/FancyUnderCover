import random
import json
import networkx as nx

def generate_random_graph(nodes, edges):
    graph = nx.Graph()
    
    # Добавляем узлы
    graph.add_nodes_from(range(1, nodes + 1))
        
    # Добавляем случайные рёбра
    for _ in range(edges):
        while True:
            edge = (random.randint(1, nodes), random.randint(1, nodes))
            if edge[0] != edge[1] and not graph.has_edge(*edge):
                graph.add_edge(*edge)
                break
            
    return graph

def convert_graph_to_visjs(graph):
    nodes = [{'id': str(node), 'label': str(node)} for node in graph.nodes()]
    edges = [{'from': str(edge[0]), 'to': str(edge[1])} for edge in graph.edges()]

    data = {'nodes': nodes, 'edges': edges}

    json_data = json.dumps(data, indent=4)
    return json_data