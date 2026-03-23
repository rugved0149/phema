from typing import Dict

from app.correlation.correlator import CorrelationContext


MAX_SIGNALS = 25  # safety limit for rendering


def build_graph(context: CorrelationContext) -> Dict:

    nodes = []
    links = []

    root_id = context.entity_id

    # -------------------------
    # ROOT ENTITY
    # -------------------------

    nodes.append({
        "id": root_id,
        "type": "entity",
        "label": root_id
    })

    module_nodes = set()
    signal_nodes = set()
    edge_set = set()

    module_counts = context.module_counts
    signal_counts = context.signal_counts

    # Track highest severity per signal
    signal_severity = {}

    severity_rank = {
        "low": 1,
        "medium": 2,
        "high": 3
    }

    # -------------------------
    # GROUP SIGNALS BY MODULE
    # -------------------------

    module_signal_map = {}

    for event in context.ordered_events:

        module = event.module.value
        signal = event.signal

        if module not in module_signal_map:
            module_signal_map[module] = set()

        module_signal_map[module].add(signal)

        # Track highest severity
        current_sev = event.severity.value
        prev_sev = signal_severity.get(signal)

        if (
            prev_sev is None
            or severity_rank[current_sev] >
            severity_rank.get(prev_sev, 0)
        ):
            signal_severity[signal] = current_sev

    # -------------------------
    # BUILD GRAPH STRUCTURE
    # -------------------------

    total_signals_added = 0

    for module_name, signals in module_signal_map.items():

        module_id = f"module:{module_name}"

        # MODULE NODE

        if module_id not in module_nodes:

            nodes.append({
                "id": module_id,
                "type": "module",
                "label": module_name,
                "count": module_counts.get(module_name, 1)
            })

            links.append({
                "source": root_id,
                "target": module_id
            })

            module_nodes.add(module_id)

        # -------------------------
        # ADD SIGNALS (LIMITED)
        # -------------------------

        for signal_name in sorted(signals):

            if total_signals_added >= MAX_SIGNALS:
                break

            # 🔥 SHORTEN LABEL SAFELY
            parts = signal_name.split(":")

            short_label = parts[-1].strip()

            if not short_label:
                short_label = signal_name

            signal_id = f"signal:{signal_name}"

            if signal_id not in signal_nodes:

                nodes.append({
                    "id": signal_id,
                    "type": "signal",
                    "label": short_label,
                    "count": signal_counts.get(signal_name, 1),
                    "severity": signal_severity.get(signal_name, "low")
                })

                signal_nodes.add(signal_id)

                total_signals_added += 1

            # MODULE → SIGNAL EDGE

            edge_key = (module_id, signal_id)

            if edge_key not in edge_set:

                links.append({
                    "source": module_id,
                    "target": signal_id,
                    "weight": signal_counts.get(signal_name, 1)
                })

                edge_set.add(edge_key)

    return {
        "nodes": nodes,
        "links": links
    }