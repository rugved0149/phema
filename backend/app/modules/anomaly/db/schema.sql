-- ================================
-- Access Events (Immutable Log)
-- ================================
CREATE TABLE IF NOT EXISTS access_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    hour INTEGER NOT NULL,
    day INTEGER NOT NULL,
    source_ip TEXT NOT NULL,
    country TEXT NOT NULL,
    asn TEXT NOT NULL,
    client_type TEXT NOT NULL,
    access_type TEXT NOT NULL,
    time_since_last REAL
);

-- ================================
-- Behavioral Baseline (Single Row)
-- ================================
CREATE TABLE IF NOT EXISTS baseline_profile (
    id INTEGER PRIMARY KEY CHECK (id = 1),

    mean_access_hour REAL,
    std_access_hour REAL,

    avg_events_per_hour REAL,
    burst_threshold REAL,

    known_countries TEXT,
    known_asns TEXT,
    known_clients TEXT,

    last_updated TEXT
);

-- ================================
-- Risk Decisions (Explainability)
-- ================================
CREATE TABLE IF NOT EXISTS risk_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER,
    risk_score REAL,
    verdict TEXT,
    reasons TEXT,
    timestamp TEXT,

    FOREIGN KEY (event_id) REFERENCES access_events(id)
);
