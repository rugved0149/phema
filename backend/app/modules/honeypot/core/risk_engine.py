# core/risk_engine.py

import time
from app.modules.honeypot.utils.paths import DB_PATH

BLOCK_THRESHOLD = 80
DECAY_INTERVAL = 60      # seconds
DECAY_AMOUNT = 10        # risk points
SHADOW_BAN_THRESHOLD = 50


class RiskEngine:
    def __init__(self):
        # { ip: {"score": int, "last_seen": timestamp} }
        self.ip_data = {}

    def _apply_decay(self, ip):
        now = time.time()

        if ip not in self.ip_data:
            return

        last_seen = self.ip_data[ip]["last_seen"]
        elapsed = now - last_seen

        decay_steps = int(elapsed // DECAY_INTERVAL)

        if decay_steps > 0:
            decay = decay_steps * DECAY_AMOUNT
            self.ip_data[ip]["score"] = max(
                0, self.ip_data[ip]["score"] - decay
            )
            self.ip_data[ip]["last_seen"] = now

    def add_score(self, ip, value):
        now = time.time()

        if ip not in self.ip_data:
            self.ip_data[ip] = {
                "score": 0,
                "last_seen": now
            }

        # apply decay before adding new risk
        self._apply_decay(ip)

        self.ip_data[ip]["score"] += value
        self.ip_data[ip]["last_seen"] = now

    def get_score(self, ip):
        self._apply_decay(ip)
        return min(self.ip_data.get(ip, {}).get("score", 0), 100)

    def should_block(self, ip):
        return self.get_score(ip) >= BLOCK_THRESHOLD

    def is_shadow_banned(self, ip):
        return SHADOW_BAN_THRESHOLD <= self.get_score(ip) < BLOCK_THRESHOLD

    def get_all_risks(self):
        return self.ip_data

risk_engine = RiskEngine()