import os

from flask import Flask, jsonify, render_template, request
from neo4j import GraphDatabase

app = Flask(__name__)

NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "changeme123")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))


def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters or {})
        return [record.data() for record in result]


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/graph", methods=["GET"])
def get_graph():
    """Return all nodes and relationships for rendering."""
    nodes_query = """
    MATCH (n)
    RETURN elementId(n) AS id, labels(n) AS labels, properties(n) AS props
    """
    rels_query = """
    MATCH (a)-[r]->(b)
    RETURN elementId(r) AS id, elementId(a) AS source, elementId(b) AS target,
           type(r) AS type, properties(r) AS props
    """
    nodes = run_query(nodes_query)
    rels = run_query(rels_query)
    return jsonify({"nodes": nodes, "relationships": rels})


@app.route("/api/node", methods=["POST"])
def create_node():
    """Create a node. Expects JSON: {label: str, properties: {...}}"""
    data = request.get_json()
    label = data.get("label", "Node")
    properties = data.get("properties", {})

    # Sanitize label - alphanumeric and underscore only, to avoid injection via label
    label = "".join(c for c in label if c.isalnum() or c == "_") or "Node"

    query = f"""
    CREATE (n:{label})
    SET n = $properties
    RETURN elementId(n) AS id, labels(n) AS labels, properties(n) AS props
    """
    result = run_query(query, {"properties": properties})
    return jsonify(result[0] if result else {})


@app.route("/api/node/<node_id>", methods=["PUT"])
def update_node(node_id):
    """Update a node's properties."""
    data = request.get_json()
    properties = data.get("properties", {})

    query = """
    MATCH (n) WHERE elementId(n) = $node_id
    SET n += $properties
    RETURN elementId(n) AS id, labels(n) AS labels, properties(n) AS props
    """
    result = run_query(query, {"node_id": node_id, "properties": properties})
    return jsonify(result[0] if result else {})


@app.route("/api/node/<node_id>", methods=["DELETE"])
def delete_node(node_id):
    """Delete a node and its relationships."""
    query = """
    MATCH (n) WHERE elementId(n) = $node_id
    DETACH DELETE n
    """
    run_query(query, {"node_id": node_id})
    return jsonify({"deleted": node_id})


@app.route("/api/relationship", methods=["POST"])
def create_relationship():
    """Create a relationship. Expects JSON: {source: id, target: id, type: str, properties: {...}}"""
    data = request.get_json()
    source = data.get("source")
    target = data.get("target")
    rel_type = data.get("type", "RELATED_TO")
    properties = data.get("properties", {})

    # Sanitize relationship type
    rel_type = "".join(c for c in rel_type if c.isalnum() or c == "_") or "RELATED_TO"

    query = f"""
    MATCH (a) WHERE elementId(a) = $source
    MATCH (b) WHERE elementId(b) = $target
    CREATE (a)-[r:{rel_type}]->(b)
    SET r = $properties
    RETURN elementId(r) AS id, type(r) AS type, properties(r) AS props
    """
    result = run_query(
        query, {"source": source, "target": target, "properties": properties}
    )
    return jsonify(result[0] if result else {})


@app.route("/api/relationship/<rel_id>", methods=["DELETE"])
def delete_relationship(rel_id):
    """Delete a relationship."""
    query = """
    MATCH ()-[r]->() WHERE elementId(r) = $rel_id
    DELETE r
    """
    run_query(query, {"rel_id": rel_id})
    return jsonify({"deleted": rel_id})


@app.route("/api/labels", methods=["GET"])
def get_labels():
    """Return distinct node labels currently in the graph, for the type dropdown."""
    query = "CALL db.labels() YIELD label RETURN label ORDER BY label"
    result = run_query(query)
    return jsonify([r["label"] for r in result])


@app.route("/api/relationship-types", methods=["GET"])
def get_relationship_types():
    """Return distinct relationship types currently in the graph."""
    query = "CALL db.relationshipTypes() YIELD relationshipType RETURN relationshipType ORDER BY relationshipType"
    result = run_query(query)
    return jsonify([r["relationshipType"] for r in result])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
