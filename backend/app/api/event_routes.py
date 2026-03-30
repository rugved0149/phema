from fastapi import APIRouter

from app.correlation.sqlite_event_store import SQLiteEventStore


router=APIRouter(prefix="/events")

store=SQLiteEventStore()


@router.get(
    "/{user_id}/{session_id}"
)

def get_session_events(

    user_id:str,
    session_id:str

):

    events=store.fetch_events(

        user_id=user_id,
        session_id=session_id

    )

    results=[]

    for e in events:

        results.append({

            "timestamp":e.timestamp,

            "module":e.module,

            "signal":e.signal,

            "severity":e.severity,

            "metadata":e.metadata

        })

    return {

        "events":results

    }