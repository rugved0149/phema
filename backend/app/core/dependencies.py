# app/core/dependencies.py

from app.correlation.sqlite_event_store import SQLiteEventStore
from app.correlation.correlator import Correlator
from app.correlation.risk_scoring import RiskScorer

event_store = SQLiteEventStore()
correlator = Correlator(event_store)
risk_scorer = RiskScorer()