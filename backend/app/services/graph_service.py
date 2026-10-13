import networkx as nx

from app.services.entity_extraction_service import (
    extract_entities
)


def build_graph():

    graph = nx.Graph()

    entities = extract_entities()

    for project in entities["projects"]:

        graph.add_node(
            project,
            group="project"
        )

    for risk in entities["risks"]:

        graph.add_node(
            risk,
            group="risk"
        )

    for action in entities["actions"]:

        graph.add_node(
            action,
            group="action"
        )

    for team in entities["teams"]:

        graph.add_node(
            team,
            group="team"
        )

    projects = entities["projects"]

    risks = entities["risks"]

    actions = entities["actions"]

    for project in projects:

        for risk in risks:

            graph.add_edge(
                project,
                risk
            )

    for risk in risks:

        for action in actions:

            graph.add_edge(
                risk,
                action
            )

    return graph