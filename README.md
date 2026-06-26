# Riskopathic


This is really a simple frontend for visual creation and editing of graph nodes and edges. My use case is for assets and cyber risk, but it is easily customized for any data.

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

## Stack

- **Neo4j Community Edition** — graph database
- **NeoDash** — dashboards for risk/exposure views
- **Custom Flask + Cytoscape.js app** — visual node/edge editor (since Neo4j Bloom requires Enterprise + a separate license, and no open-source drag-and-drop graph editor exists for Neo4j)

All three run as containers on a shared Docker network.

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
| Neo4j Browser | http://localhost:7474 | Raw Cypher queries |
| NeoDash | http://localhost:5005 | Dashboards and reports |
| Bolt | bolt://localhost:7687 | Driver connections |

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
- NeoDash is unmaintained upstream (Neo4j Labs deprecated it); still functional for self-hosted use, just no future patches.
