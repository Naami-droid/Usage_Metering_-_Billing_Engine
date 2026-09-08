from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from fastapi import HTTPException
from models import UsageEvents, Subscriptions, Plans

from models import UsageEvents 


def check_tenant_limit(db:Session, tenant_id:UUID, usage_type:str)->int:
    limit=db.query(func.sum(UsageEvents.quantity)).filter(
        UsageEvents.tenant_id==tenant_id , UsageEvents.usage_type == usage_type
    ).scalar()
    if limit==None:
        return 0
    else:
        return limit

def verify_token_allowance(db:Session, tenant_id:UUID, usage_type:str):
    sub_status=db.query(Subscriptions.status).filter(
        Subscriptions.tenant_id == tenant_id
    ).scalar()
    if sub_status !="active":
        raise HTTPException(402, "PAYMENT REQUIRED!")
    tenant_usage=check_tenant_limit(db, tenant_id,  usage_type)
    plan_id=db.query(Subscriptions.plan_id).filter(
        Subscriptions.tenant_id==tenant_id
    ).scalar()
    plan_api_limit, plan_ai_token=db.query(Plans.api_call_limit, Plans.ai_token_limit).filter(
        Plans.id==plan_id
    ).first()
    if usage_type=="api_call":
        if tenant_usage>= plan_api_limit:
            raise HTTPException(status_code=402, detail="Payment Required. Out of api call limit!")
    if usage_type =="ai_tokens":
            if tenant_usage>= plan_ai_token:
                raise HTTPException(status_code=402, detail="Payment Required. Out of ai tokens!")
    return True