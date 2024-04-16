from flask import Flask, render_template, request, jsonify

import graph as G
from darwin_genetic import Darwin

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
def add() -> jsonify:
    global MY_GRAPH
    
    stop_count = request.args.get('iters', type=int)
    agents_count = request.args.get('agents', type=int)
    
    if stop_count is not None and agents_count is not None:
        my_darwin = Darwin(MY_GRAPH, agents_count, stop_count)
        my_darwin.take_score()

        for _ in range(my_darwin.stop_point):
            my_darwin.iteration()
        return jsonify({'result': list(my_darwin.get_best().vertex_by_string_set())})
    else:
        return jsonify({'error': 'Missing parameters'})


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
