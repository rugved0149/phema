# app/core/dependencies.py

from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer


# -------------------------
# SINGLETON OBJECTS
# -------------------------

# Create store first
event_store = SQLiteEventStore()

# Pass same store into correlator
correlator = Correlator(event_store)

# Risk scorer
risk_scorer = RiskScorer()