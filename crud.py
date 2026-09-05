from models import Tenant, Subscriptions
from sqlalchemy.orm import Session


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


