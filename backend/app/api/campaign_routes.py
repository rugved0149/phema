from fastapi import APIRouter

from app.correlation.campaign_intelligence import CampaignIntelligence


router=APIRouter(prefix="/campaign")


engine=CampaignIntelligence()


@router.get("/active")

def get_campaigns():

    return engine.get_active_campaigns()