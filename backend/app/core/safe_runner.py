import logging
from app.api.user_routes import update_session_status

def run_safe(module_name,func,*args,**kwargs):
    session_id=None
    if len(args)>1:
        session_id=args[1]

    if session_id:
        update_session_status(
            session_id,
            "PROCESSING"
        )

    try:
        result=func(*args,**kwargs)
        if session_id:
            update_session_status(
                session_id,
                "COMPLETED"
            )
        return result

    except Exception as e:
        logging.error(
            f"[MODULE FAILURE] {module_name}: {str(e)}"
        )
        if session_id:
            update_session_status(
                session_id,
                "FAILED"
            )

        return None