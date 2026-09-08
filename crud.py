from models import Tenant, Subscriptions, UsageEvents
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import UUID

def create_Tenant(db: Session , name: str):
# Instantiate sqlalchemy model with tenant data (in computer)
    db_tenant=Tenant(name=name)

    # giving that to sqlalchemy it stores temporarily
    db.add(db_tenant)

    #now sqlalchmey pushes that to supabase

    db.commit()


    #now we fetch the latest state of the row

    db.refresh(db_tenant)

    db_subscription=Subscriptions(
        tenant_id=db_tenant.id,
        plan_id="free",
        status="active"
    )
    db.add(db_subscription)
    db.commit()

    return db_tenant

def record_usage_event(db: Session, tenant_id: UUID, usage_type: str, quantity: int, idempotency_key: str):
    # first we need to check that if the idempotency key already exists 
    existing_key=db.query(UsageEvents).filter(
        UsageEvents.idempotency_key==idempotency_key
    ).first()
    if existing_key:
        return existing_key
    else:
        db_newevent=UsageEvents(
            tenant_id=tenant_id,
            usage_type=usage_type,
            quantity=quantity,
            idempotency_key=idempotency_key
        )
        db.add(db_newevent)
        db.commit()
        db.refresh(db_newevent)

        return db_newevent
    