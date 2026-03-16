def emit_phema_event(entity_id, entity_type, signal, confidence, severity, metadata):
    return {
        "entity_id": str(entity_id),
        "entity_type": entity_type,
        "module": "anomaly",
        "signal": signal,
        "confidence": round(float(confidence), 3),
        "severity": severity,
        "metadata": metadata,
    }
