from flask import Flask, render_template, request, jsonify
import networkx as nx

app = Flask(__name__)

# Sample flight graph
flight_graph = nx.DiGraph()
flight_graph.add_weighted_edges_from([
    ("JFK", "LAX", 360),
    ("JFK", "ORD", 120),
    ("ORD", "LAX", 240),
    ("LAX", "SFO", 60),
    ("ORD", "DFW", 150),
    ("DFW", "LAX", 180),
    ("JFK", "MIA", 180),
    ("MIA", "LAX", 300)
])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/find_route", methods=["POST"])
def find_route():
    data = request.json
    source = data.get("source")
    destination = data.get("destination")

    if source not in flight_graph or destination not in flight_graph:
        return jsonify({"error": "Invalid airport code!"}), 400

    try:
        path = nx.shortest_path(flight_graph, source, destination, weight="weight")
        travel_time = nx.shortest_path_length(flight_graph, source, destination, weight="weight")
        return jsonify({"path": path, "travel_time": travel_time})
    except nx.NetworkXNoPath:
        return jsonify({"error": "No available route!"}), 404

if __name__ == "__main__":
    app.run(debug=True)
