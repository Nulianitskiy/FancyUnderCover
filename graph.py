"""Модуль для создания случайного графа и работы с ним в vis.js"""

import random
import json
import networkx as nx


def generate_random_graph(nodes, edges):
    """Создать случайный граф по параметрам

    Args:
        nodes (int): Количество вершин
        edges (int): Количество ребер

    Returns:
        nx.Graph: Граф networkx
    """
    graph = nx.Graph()
    
    # Добавляем узлы
    for node in range(1, nodes):
        graph.add_node(node)
        
    # Добавляем случайные рёбра
    edge_list = []
    for _ in range(edges):
        while True:
            edge = (random.randint(1, nodes), random.randint(1, nodes))
            if edge not in edge_list and edge[0] != edge[1]:
                edge_list.append(edge)
                graph.add_edge(edge[0], edge[1])
                break
            
    return graph

def convert_graph_to_visjs(graph):
    """Конвертировать граф networkx в json для vis.js

    Args:
        graph (nx.Graph): Граф

    Returns:
        json: json для vis.js
    """
    nodes = []
    edges = []

    for node in graph.nodes():
        node_data = {'id': str(node), 'label': str(node)}  # Используем строковые идентификаторы
        nodes.append(node_data)

    for edge in graph.edges():
        edge_data = {'from': str(edge[0]), 'to': str(edge[1])}
        edges.append(edge_data)

    data = {'nodes': nodes, 'edges': edges}

    json_data = json.dumps(data, indent=4)
    return json_data