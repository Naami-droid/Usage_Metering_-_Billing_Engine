from sqlalchemy import Column , String, DateTime, func, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Relationship
import uuid
from database import Base


class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=Column(String, nullable=False)
    created_at =Column(DateTime(timezone=True),  server_default=func.now())
    stripe_customer_id =  Column(String, nullable=True)

class Plans(Base):
    __tablename__ ="plans"
    id=Column(String, primary_key=True, default='free')
    name=Column(String)
    api_call_limit=Column(Integer)
    ai_token_limit=Column(Integer)
    price_in_cents=Column(Integer)

class Subscriptions(Base):
    __tablename__="subscriptions"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id=Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    plan_id=Column(String, ForeignKey("plans.id"), nullable=False)
    status=Column(String, default='active')
    stripe_subscription_id=Column(String, nullable=True)

class UsageEvents(Base):
    __tablename__="usage_events"
    id=Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id=Column(UUID(as_uuid=True), ForeignKey("tenants.id"),nullable=False )
    usage_type=Column(String, nullable=False)
    quantity=Column(Integer)
    idempotency_key=Column(String, nullable=False)
    created_at=Column(DateTime(timezone=True), server_default=func.now())
    