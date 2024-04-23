var network;

document.addEventListener('DOMContentLoaded', function() {
    var container = document.getElementById('graph-container');
    var form = document.getElementById('graph-form');
    var dform = document.getElementById('darwin-form');

    var darwinButton = document.getElementById('darwin-btn')
    var devriesButton = document.getElementById('devries-btn')

    function updateGraph(n_nodes, n_edges) {
        var url = '/graph?n_nodes=' + encodeURIComponent(n_nodes) + '&n_edges=' + encodeURIComponent(n_edges);

        fetch(url)
            .then(response => response.json())
            .then(data => {
                var nodes = new vis.DataSet(data.nodes);
                var edges = new vis.DataSet(data.edges);

                var graphData = {
                    nodes: nodes,
                    edges: edges
                };

                var options = {
                    layout: {
                        hierarchical: false,
                    },
                    physics: {
                        enabled: false,
                    }
                };

                network = new vis.Network(container, graphData, options);
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных графа:', error);
            });
    }

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        var n_nodes = document.getElementById('n_nodes').value;
        var n_edges = document.getElementById('n_edges').value;
        updateGraph(n_nodes, n_edges);
    });

    updateGraph('5', '6');

    function updateDarwin(agents, iters) {
        var durl = '/darwin?agents=' + encodeURIComponent(agents) + '&iters=' + encodeURIComponent(iters);
    
        fetch(durl)
            .then(response => response.json())
            .then(data => {
                const results = data.vis;

                const message = `Результаты Darwin: Счет${data.score}`;
                const resultTextElement = document.getElementById('result-text')
                resultTextElement.textContent = message;
    
                var nodes = network.body.data.nodes;
                var edges = network.body.data.edges;
    
                // Обновление цветов вершин в зависимости от результатов
                nodes.forEach(node => {
                    if (results.includes(node.id)) {
                        node.color = { background: "#FFD6D6", border: "#FF0000" }; // Постельный оттенок красного
                    } else {
                        node.color = { background: "#97C2FC", border: "#2B7CE9" }; // Голубой
                    }
                });
    
                var updatedNodes = new vis.DataSet(nodes.get());
                var updatedEdges = new vis.DataSet(edges.get());

                updatedEdges.forEach(edge => {
                    var fromNode = updatedNodes.get(edge.from);
                    var toNode = updatedNodes.get(edge.to);
                    
                    if (fromNode.color && fromNode.color.border === "#FF0000") {
                        edge.color = { color: "#FF0000" }; // Красный цвет для ребра
                    } else if (toNode.color && toNode.color.border === "#FF0000") {
                        edge.color = { color: "#FF0000" }; // Красный цвет для ребра
                    } else {
                        edge.color = { color: "#2B7CE9" }; // Голубой цвет для остальных ребер
                    }
                });

                var graphData = {
                    nodes: updatedNodes,
                    edges: updatedEdges
                };

                // Обновляем данные графа и перерисовываем сеть
                network.setData(graphData);
    
                // Перерисовываем сеть
                network.redraw();
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных Darwin:', error);
            });
    }
    

    darwinButton.addEventListener('click', function(event) {
        event.preventDefault();
        var agents = document.getElementById('agents').value;
        var iters = document.getElementById('iters').value;
        updateDarwin(agents, iters);
    });


    function updateDevries(agents, iters) {
        var durl = '/devries?agents=' + encodeURIComponent(agents) + '&iters=' + encodeURIComponent(iters);
    
        fetch(durl)
            .then(response => response.json())
            .then(data => {
                const results = data.vis;
                const message = `Результаты De Vries: Счет: ${data.score} Катастроф: ${data.dooms}`;
                const resultTextElement = document.getElementById('result-text')
                resultTextElement.textContent = message;
    
                var nodes = network.body.data.nodes;
                var edges = network.body.data.edges;
    
                // Обновление цветов вершин в зависимости от результатов
                nodes.forEach(node => {
                    if (results.includes(node.id)) {
                        node.color = { background: "#FFD6D6", border: "#FF0000" }; // Постельный оттенок красного
                    } else {
                        node.color = { background: "#97C2FC", border: "#2B7CE9" }; // Голубой
                    }
                });
    
                var updatedNodes = new vis.DataSet(nodes.get());
                var updatedEdges = new vis.DataSet(edges.get());

                updatedEdges.forEach(edge => {
                    var fromNode = updatedNodes.get(edge.from);
                    var toNode = updatedNodes.get(edge.to);
                    
                    if (fromNode.color && fromNode.color.border === "#FF0000") {
                        edge.color = { color: "#FF0000" }; // Красный цвет для ребра
                    } else if (toNode.color && toNode.color.border === "#FF0000") {
                        edge.color = { color: "#FF0000" }; // Красный цвет для ребра
                    } else {
                        edge.color = { color: "#2B7CE9" }; // Голубой цвет для остальных ребер
                    }
                });

                var graphData = {
                    nodes: updatedNodes,
                    edges: updatedEdges
                };

                // Обновляем данные графа и перерисовываем сеть
                network.setData(graphData);
    
                // Перерисовываем сеть
                network.redraw();
            })
            .catch(error => {
                console.error('Ошибка при загрузке данных Devries:', error);
            });
    }

    devriesButton.addEventListener('click', function(event) {
        event.preventDefault();
        var agents = document.getElementById('agents').value;
        var iters = document.getElementById('iters').value;
        updateDevries(agents, iters);
    });
});
