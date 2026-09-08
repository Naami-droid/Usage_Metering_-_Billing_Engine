from crud import record_usage_event
from database import get_db
from schemas import createUsageEvents, responseUsageEvents


from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session

app=APIRouter()

@app.post("/", response_model=responseUsageEvents)
def record_usage_event(db:Session = Depends(get_db), payload:createUsageEvents = Body(...)):
    new_event=record_usage_event(db=db, payload=payload)
    return new_event