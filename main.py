from flask import Flask, render_template, request, jsonify
import time

import graph as G
from darwin_genetic import Darwin
from devries_genetic import Devries

app = Flask(__name__)

MY_GRAPH = None

@app.route('/graph', methods=['GET'])
def graph() -> jsonify:
    global MY_GRAPH
    
    nodes = request.args.get('n_nodes', type=int)
    edges = request.args.get('n_edges', type=int)
    if nodes is not None and edges is not None:
        MY_GRAPH = G.generate_random_graph(nodes,edges)
        return G.convert_graph_to_visjs(MY_GRAPH)
    else:
        return jsonify({'error': 'Проблемы с параметрами'})

@app.route('/darwin', methods=['GET'])
def add_darwin() -> jsonify:
    global MY_GRAPH
    
    stop_count = request.args.get('iters', type=int)
    agents_count = request.args.get('agents', type=int)
    
    if stop_count is not None and agents_count is not None:
        start_time = time.time()
        
        my_darwin = Darwin(MY_GRAPH, agents_count, stop_count)
        my_darwin.take_score()

        for _ in range(my_darwin.stop_point):
            my_darwin.iteration()
        
        end_time = time.time()
        stash = list(my_darwin.res_stash)
        res = my_darwin.get_best()
        return jsonify({'vis': list(res.vertex_by_string_set()), 'score': res.score, 'stash': stash, 'time': end_time - start_time})
    else:
        return jsonify({'error': 'Missing parameters'})

@app.route('/devries', methods=['GET'])
def add_devries() -> jsonify:
    global MY_GRAPH
    
    stop_count = request.args.get('iters', type=int)
    agents_count = request.args.get('agents', type=int)
    
    if stop_count is not None and agents_count is not None:
        start_time = time.time()
        
        my_devries = Devries(MY_GRAPH, agents_count, stop_count)
        my_devries.take_score()

        for _ in range(my_devries.stop_point):
            my_devries.iteration()
        
        end_time = time.time()
        stash = list(my_devries.res_stash)
        res = my_devries.get_best()
        return jsonify({'vis': list(res.vertex_by_string_set()), 'score': res.score, 'stash': stash, 'time': end_time - start_time, 'dooms': my_devries.doom_count})
    else:
        return jsonify({'error': 'Missing parameters'})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
