import logging
import traceback
from app.api.user_routes import update_session_status


def run_safe(module_name, func, *args, **kwargs):

    session_id = None

    if len(args) > 1:
        session_id = args[1]

    try:

        result = func(*args, **kwargs)

        return result

    except Exception as e:

        logging.error(
            f"[MODULE FAILURE] {module_name}: {str(e)}"
        )

        traceback.print_exc()

        if session_id:

            update_session_status(
                session_id,
                "FAILED"
            )

        return None