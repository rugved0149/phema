from typing import Optional, Dict

from app.modules.phishing.engine import run_phishing
from app.modules.honeypot.engine import run_honeypot
from app.modules.file_checker.engine import run_file_scan
from app.modules.anomaly.engine import run_anomaly
from app.modules.tone.engine import run_tone_analysis

from app.core.safe_runner import run_safe
from app.api.user_routes import update_session_status


class PHEMAEngine:

    def run(
        self,
        *,
        user_id: str,
        session_id: str,
        entity_id: str,
        entity_type: str,
        url=None,
        text=None,
        file_path=None,
        session_context=None
    ):

        update_session_status(
            session_id,
            "PROCESSING"
        )

        try:

            if url:

                run_safe(
                    "phishing",
                    run_phishing,
                    user_id,
                    session_id,
                    url,
                    entity_id
                )

            if (
                session_context
                and session_context.get("access_type")
                in ["probe", "unauthorized"]
                and "ip" in session_context
            ):

                run_safe(
                    "honeypot",
                    run_honeypot,
                    user_id,
                    session_id,
                    session_context["ip"],
                    entity_id
                )

            if file_path:

                print(
                    "FILE SCAN TRIGGERED:",
                    file_path
                )

                run_safe(
                    "file_checker",
                    run_file_scan,
                    user_id,
                    session_id,
                    file_path,
                    entity_id
                )

            if (
                session_context
                and session_context.get("access_type")
                in ["multiple_failures", "suspicious_login"]
            ):

                run_safe(
                    "anomaly",
                    run_anomaly,
                    user_id,
                    session_id,
                    entity_id,
                    session_context
                )

            if text:

                run_safe(
                    "tone",
                    run_tone_analysis,
                    user_id,
                    session_id,
                    text,
                    entity_id
                )

            update_session_status(
                session_id,
                "COMPLETED"
            )

        except Exception:

            update_session_status(
                session_id,
                "FAILED"
            )

            raise