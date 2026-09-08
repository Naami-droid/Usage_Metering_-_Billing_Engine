from schemas import chatRequest

from fastapi import APIRouter, Depends, Body , Header
from sqlalchemy.orm import Session

from database import get_db

import crud 
import services
import utils

router=APIRouter()

@router.post("/chat")
def generate_ai_response(
    payload:chatRequest = Body(...),
    db:Session=Depends(get_db),
    x_request_id:str=Header(...)
):
    # recording the api call
    # Check
    api_limit_check=services.verify_token_allowance(db,payload.tenant_id, "api_call" )
    # Prepare
    idempotency_key=utils.create_idempotency_key(x_request_id, 'api_call')
    # Write
    crud.record_usage_event(db,payload.tenant_id,"api_call",1,idempotency_key)

    #recording the ai tokens
    # Check
    ai_token_limit=services.verify_token_allowance(db, payload.tenant_id, "ai_tokens")
    #Prepare
    token_count=utils.simulate_token_count(payload.prompt)
    idempotency_key=utils.create_idempotency_key(x_request_id, "ai_tokens")
    # Write
    crud.record_usage_event(db,payload.tenant_id,"ai_tokens", token_count,idempotency_key)

