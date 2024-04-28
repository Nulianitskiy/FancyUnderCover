from flask import Flask, render_template, request, jsonify
import time

import graph as G
from darwin_genetic import Darwin
from devries_genetic import Devries

app = Flask(__name__)

MY_GRAPH = None

@app.route('/graph', methods=['GET'])
def graph():
    global MY_GRAPH

    nodes = request.args.get('n_nodes', type=int)
    edges = request.args.get('n_edges', type=int)
    
    if nodes is not None and edges is not None:
        MY_GRAPH = G.generate_random_graph(nodes, edges)
        return G.convert_graph_to_visjs(MY_GRAPH)
    else:
        return jsonify({'error': 'Проблемы с параметрами'})

def run_genetic_algorithm(algorithm_cls, agents_count, stop_count):
    global MY_GRAPH
    start_time = time.time()
    algorithm = algorithm_cls(MY_GRAPH, agents_count, stop_count)
    algorithm.take_score()

    for _ in range(algorithm.stop_point):
        algorithm.iteration()

    end_time = time.time()
    
    return algorithm, end_time - start_time

@app.route('/darwin', methods=['GET'])
def add_darwin():
    agents_count = request.args.get('agents', type=int)
    stop_count = request.args.get('iters', type=int)
    
    if agents_count is not None and stop_count is not None:
        model, time = run_genetic_algorithm(Darwin, agents_count, stop_count)
        res = model.get_best()
        return jsonify({'vis': list(res.vertex_by_string_set()), 'score': res.score, 'stash': list(model.res_stash), 'time': time})
    else:
        return jsonify({'error': 'Отсутствуют параметры'})

@app.route('/devries', methods=['GET'])
def add_devries():
    agents_count = request.args.get('agents', type=int)
    stop_count = request.args.get('iters', type=int)
    
    if agents_count is not None and stop_count is not None:
        model, time = run_genetic_algorithm(Devries, agents_count, stop_count)
        res = model.get_best()
        return jsonify({'vis': list(res.vertex_by_string_set()), 'score': res.score, 'stash': list(model.res_stash), 'time': time, 'dooms': model.doom_count})
    else:
        return jsonify({'error': 'Отсутствуют параметры'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
