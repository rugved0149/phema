# app/orchestrator/phema_engine.py

from typing import Optional, Dict

from app.modules.phishing.engine import run_phishing
from app.modules.honeypot.engine import run_honeypot
from app.modules.file_checker.engine import run_file_scan
from app.modules.anomaly.engine import run_anomaly
from app.modules.tone.engine import run_tone_analysis
from app.core.safe_runner import run_safe


class PHEMAEngine:
    """
    Central orchestrator that triggers detection modules.
    """

    def run(
        self,
        *,
        entity_id: str,
        entity_type: str,
        url: Optional[str] = None,
        text: Optional[str] = None,
        file_path: Optional[str] = None,
        session_context: Optional[Dict] = None
    ):

        if url:
            run_safe("phishing", run_phishing, url, entity_id)

        if session_context and "ip" in session_context:
            run_safe(
                "honeypot",
                run_honeypot,
                session_context["ip"],
                entity_id
            )

        if file_path:
            run_safe(
                "file_checker",
                run_file_scan,
                file_path,
                entity_id
            )

        if session_context:
            run_safe(
                "anomaly",
                run_anomaly,
                entity_id,
                session_context
            )

        if text:
            run_safe(
                "tone",
                run_tone_analysis,
                text,
                entity_id
            )