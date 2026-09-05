from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict 

class CustomerCreation(BaseModel):
    name: str = Field(description='Name of the tenant')

class CustCreatConf(BaseModel):
    id:UUID
    name : str
    created_at: datetime
    stripe_customer_id: str | None= None

    # This configuration tells Pydantic it's okay to read data directly from SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)

class recordingUsageEvents(BaseModel):
    tenant_id : UUID
    usage_type: str = Field(description='whether the request is api call or ai tokens')
    idempotency_key: str 
    quantity: int

class responseUsageEvent(BaseModel):
    tenant_id: UUID
    usage_type :str
    idempotency_key: str
    quantity: str

class viewSubscriptionRequest(BaseModel):
    tenant_id : UUID
    plan_id : str

class viewSubscriptionResponse(BaseModel):
    tenant_id: UUID
    plan_id: str
    api_call_limit: int
    ai_token_limit: int

class planChange(BaseModel):
    plan_id : str = Field(description= 'The plan they want to change')

class planChangeResponse(BaseModel):
    plan_id: str
    name : str
    api_call_limit:int
    ai_token_limit:int
    price_in_cents: int

class subscriptionUsageResponse(BaseModel):
    tenant_id: UUID
    total_api_calls_made: int
    total_ai_tokens_used: int
    api_call_limit: int
    ai_token_limit:int
