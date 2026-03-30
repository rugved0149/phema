from sqlalchemy import func
from app.db.base import SessionLocal
from app.db.session import EventRecord


class CampaignIntelligence:

    def get_reused_urls(self):

        with SessionLocal() as db:

            rows=(
                db.query(
                    EventRecord.signal,
                    func.count(
                        func.distinct(
                            EventRecord.user_id
                        )
                    ).label("user_count")
                )
                .filter(
                    EventRecord.signal.like(
                        "phishing:%"
                    )
                )
                .group_by(
                    EventRecord.signal
                )
                .having(
                    func.count(
                        func.distinct(
                            EventRecord.user_id
                        )
                    )>=2
                )
                .all()
            )

            campaigns=[]

            for r in rows:

                campaigns.append({

                    "signal":r.signal,

                    "users_affected":r.user_count

                })

            return campaigns


    def get_reused_files(self):

        with SessionLocal() as db:

            rows=(
                db.query(
                    EventRecord.signal,
                    func.count(
                        func.distinct(
                            EventRecord.user_id
                        )
                    ).label("user_count")
                )
                .filter(
                    EventRecord.signal.like(
                        "file:%"
                    )
                )
                .group_by(
                    EventRecord.signal
                )
                .having(
                    func.count(
                        func.distinct(
                            EventRecord.user_id
                        )
                    )>=2
                )
                .all()
            )

            campaigns=[]

            for r in rows:

                campaigns.append({

                    "signal":r.signal,

                    "users_affected":r.user_count

                })

            return campaigns


    def get_active_campaigns(self):

        phishing=self.get_reused_urls()

        files=self.get_reused_files()

        return {

            "phishing_campaigns":phishing,

            "file_campaigns":files

        }