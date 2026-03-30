# app/core/context.py

from contextvars import ContextVar

# Context variables

current_user: ContextVar[str] = ContextVar(
    "current_user",
    default="system"
)

current_session: ContextVar[str] = ContextVar(
    "current_session",
    default="default"
)


def set_current_context(
    user_id: str,
    session_id: str
):
    """
    Set context before running modules.
    """
    current_user.set(user_id)
    current_session.set(session_id)


def get_current_context():
    """
    Retrieve active context.
    """
    return {
        "user_id": current_user.get(),
        "session_id": current_session.get()
    }