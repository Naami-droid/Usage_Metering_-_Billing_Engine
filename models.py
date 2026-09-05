from sqlalchemy import Column , String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from database import Base


class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name=Column(String, nullable=False)
    created_at =Column(DateTime(timezone=True),  server_default=func.now())
    stripe_customer_id =  Column(String, nullable=True)

# class Plans(Base):
#     __tablename__ ="plans"