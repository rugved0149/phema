# app/core/event_emitter.py

from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.threat_memory import threat_memory
from app.correlation.event_deduplicator import event_deduplicator
from app.core.event_bus import event_bus

event_store = SQLiteEventStore()

def emit_event(event):

    if event_deduplicator.is_duplicate(event):
        return

    event_store.add_event(event)
    threat_memory.record_event(event)
    
event_bus.subscribe(emit_event)