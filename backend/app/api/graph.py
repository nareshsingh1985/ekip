from fastapi import APIRouter

from app.services.graph_service import (
    build_graph
)

router = APIRouter()


@router.get("/graph")
def graph():

    knowledge_graph = build_graph()

    nodes = []

    links = []

    for node, data in knowledge_graph.nodes(
        data=True
    ):

        nodes.append(
            {
                "id": node,
                "label": node,
                "group": data.get(
                    "group",
                    "default"
                ),
            }
        )

    for source, target, edge_data in (
        knowledge_graph.edges(data=True)
    ):

        links.append(
            {
                "source": source,
                "target": target,
                "label": edge_data.get("relation", "related to"),
            }
        )

    return {
        "nodes": nodes,
        "edges": links,
    }