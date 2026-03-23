"""
PHEMA Configuration File
------------------------

Central place for system tuning.

All thresholds, limits, and behavioral parameters
should be defined here instead of hardcoding values.

Modify values here to tune system sensitivity.
"""

# 🧱 SYSTEM SETTINGS

SYSTEM_NAME = "PHEMA Security Platform"
SYSTEM_VERSION = "1.0.0"
DEBUG_MODE = True
LOG_LEVEL = "INFO"

# 🗄️ DATABASE SETTINGS

DATABASE_URL = "sqlite:///./phema.db"

# Retain events for this duration
EVENT_RETENTION_MINUTES = 1440  # 24 hours

# Cleanup interval
EVENT_PURGE_INTERVAL_SECONDS = 600  # 10 minutes

# 🔁 EVENT PIPELINE SETTINGS

# Deduplication window
DEDUP_WINDOW_SECONDS = 10

# Maximum repeated signals per window
MAX_EVENTS_PER_WINDOW = 5

# Event emission debug printing
ENABLE_EVENT_LOGGING = True

# ⚖️ RISK SCORING SETTINGS

# Max score limits per category
MAX_MODULE_SCORE = 20
MAX_SEVERITY_SCORE = 30
MAX_BEHAVIOR_SCORE = 40
MAX_REPEAT_SCORE = 15
MAX_MEMORY_SCORE = 15

# Risk thresholds
HIGH_RISK_THRESHOLD = 75
MEDIUM_RISK_THRESHOLD = 40

# Honeypot base score
HONEYPOT_BASE_SCORE = 20

# Chain detection bonus
CHAIN_SCORE_BONUS = 10

# Campaign bonus
CAMPAIGN_SCORE_BONUS = 10

# 🧠 CORRELATION SETTINGS

# Minimum signals to consider repeated
REPEAT_SIGNAL_THRESHOLD = 2

# Maximum correlation window
DEFAULT_CORRELATION_WINDOW_MINUTES = 30

# Max correlation window
MAX_CORRELATION_WINDOW_MINUTES = 1440

# 🎯 CAMPAIGN DETECTION SETTING

# Signals required to mark campaign
CAMPAIGN_SIGNAL_THRESHOLD = 5

# Time window for campaign grouping
CAMPAIGN_TIME_WINDOW_SECONDS = 300

# 🧬 THREAT MEMORY SETTINGS

# Activity threshold
PERSISTENT_ACTIVITY_THRESHOLD = 5

# Memory decay interval
MEMORY_DECAY_INTERVAL_SECONDS = 3600

# Memory decay factor
MEMORY_DECAY_FACTOR = 0.5

# 📊 GRAPH SETTINGS

# Base node size
GRAPH_BASE_NODE_SIZE = 6

# Module size multiplier
GRAPH_MODULE_SIZE_FACTOR = 2

# Signal size multiplier
GRAPH_SIGNAL_SIZE_FACTOR = 1.5

# Edge thickness multiplier
GRAPH_EDGE_WEIGHT_FACTOR = 1.0

# 📈 TIMELINE SETTINGS

# Phase mapping
TIMELINE_PHASE_MAP = {

    "phishing": "Recon",
    "tone": "Delivery",
    "file_checker": "Execution",
    "honeypot": "Interaction",
    "anomaly": "Post-Access"
}

# 🔍 MODULE-SPECIFIC SETTINGS

# File Checker
FILE_SCAN_MAX_STRINGS = 5
FILE_ENTROPY_THRESHOLD = 7.0

# Tone Analysis
TONE_HIGH_CONFIDENCE_THRESHOLD = 0.75

# Honeypot
HONEYPOT_MIN_TRIGGER_SCORE = 10

# Phishing
PHISHING_DEFAULT_CONFIDENCE = 0.7

# 🌐 API SETTINGS

# Rate limiting
MAX_REQUESTS_PER_MINUTE = 10

# Live feed settings
LIVE_FEED_LIMIT = 20

LIVE_FEED_REFRESH_SECONDS = 3

# 🧪 TESTING SETTINGS

ENABLE_TEST_MODE = False
SIMULATION_DELAY_SECONDS = 1
MAX_TEST_EVENTS = 100

# 🔐 SECURITY SETTINGS

# Allow cross-origin requests
ENABLE_CORS = True

# API timeout
API_TIMEOUT_SECONDS = 30

# ⚙️ PERFORMANCE SETTINGS

# Max events per query
MAX_QUERY_RESULTS = 1000

# Query batch size
QUERY_BATCH_SIZE = 200

# Background cleanup enabled
ENABLE_BACKGROUND_PURGE = True