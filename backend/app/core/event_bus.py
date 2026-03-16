# app/core/event_bus.py

from typing import Callable, List
from app.correlation.schemas import CorrelationEvent


class EventBus:

    def __init__(self):
        self.subscribers: List[Callable] = []

    def subscribe(self, handler: Callable):
        """
        Register a handler that will process events.
        """
        self.subscribers.append(handler)

    def publish(self, event: CorrelationEvent):
        """
        Send event to all subscribers.
        """
        for handler in self.subscribers:
            handler(event)


# singleton event bus
event_bus = EventBus()