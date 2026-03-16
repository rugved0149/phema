# app/correlation/graph_engine.py

from typing import Dict, List
from app.correlation.correlator import CorrelationContext


def build_graph(context: CorrelationContext) -> Dict:

    nodes = []
    edges = []

    root_id = "entity"

    nodes.append({
        "id": root_id,
        "type": "entity"
    })

    # modules
    for module in context.modules_involved:

        node_id = f"module:{module}"

        nodes.append({
            "id": node_id,
            "type": "module"
        })

        edges.append({
            "from": root_id,
            "to": node_id
        })

    # signals
    for signal in context.signals:

        node_id = f"signal:{signal}"

        nodes.append({
            "id": node_id,
            "type": "signal"
        })

        edges.append({
            "from": root_id,
            "to": node_id
        })

    return {
        "nodes": nodes,
        "edges": edges
    }