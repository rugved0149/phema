from app.modules.anomaly.detection.signals import (
    time_deviation_signal,
    new_network_signal,
    burst_signal,
)


def evaluate_signals(event):
    """
    Returns list of raw deviation signals.
    Does NOT compute risk.
    """

    results = []

    signals = [time_deviation_signal, new_network_signal, burst_signal]

    for signal_fn in signals:
        deviation = signal_fn(event)
        if deviation:
            results.append(deviation)

    return results
