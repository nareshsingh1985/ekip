import networkx as nx

from app.services.entity_extraction_service import (
    extract_entities
)


def build_graph():
    graph = nx.Graph()
    entities = extract_entities()

    for group in ("projects", "risks", "actions", "teams", "applications"):
        for entity in entities.get(group, []):
            graph.add_node(entity, group=group[:-1] if group.endswith("s") else group)

    for relationship in entities.get("relationships", []):
        source = relationship["source"]
        target = relationship["target"]
        if source in graph and target in graph:
            graph.add_edge(
                source,
                target,
                relation=relationship.get("relation", "related to"),
            )

    return graph