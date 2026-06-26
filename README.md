# Riskopathic

This is really a simple app for visual creation and editing of graph nodes and edges in Neo4j. My use case is for assets and cyber risk, but it is easily customized for any data.

**Great for:**

- Single-user
- Creating/Editing/Removing a small amount of nodes and relationships manually
- A visual validation of data in Neo4j
- Simple graph CRUD operations
- Cats

**Not great for:**

- Multi-User/Concurrency
- Operations on multiple nodes/edges
- Querying data
- Anything complex

## Composition

** Custom Flask + Cytoscape.js app** — visual node/edge editor (since Neo4j Bloom requires Enterprise + a separate license, and no open-source drag-and-drop graph editor exists for Neo4j)

This requires that a Neo4j database is accessible to the container. 

## Setup

```bash
git clone https://github.com/usarmyjoe/riskopathic.git
cd riskopathic
docker compose up -d --build
```

Update `NEO4J_PASSWORD` in `docker-compose.yml` before running — don't use the default in any shared or public environment.

## Access

| Tool | URL | Purpose |
|------|-----|---------|
| Graph Editor | http://localhost:8080 | Visual node/edge creation |

## Using the Graph Editor

- Click empty canvas → create a node (set label/type and properties)
- Double-click a node → edit or delete it
- "Connect Nodes" → click two nodes in sequence → create a relationship between them
- Select an element + "Delete Selected" → remove it

Data writes directly to Neo4j over Bolt, so Browser and NeoDash reflect changes immediately.

## Schema

No fixed schema enforced yet — node labels and relationship types are free text. Suggested starting model for risk scenarios:

**Node types:** `Asset`, `Vulnerability`, `ThreatActor`, `Scenario`

**Relationship types:** `EXPOSES`, `DEPENDS_ON`, `COMPROMISES`, `MITIGATES`

## Notes

- Built for single-user / small-team scale — no clustering or HA needed.
