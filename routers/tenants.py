from crud import create_Tenant
from database import get_db
from schemas import CustomerCreation, CustCreatConf

from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session


router=APIRouter()

@router.post('/', response_model=CustCreatConf)
def register_tenant(payload:CustomerCreation = Body(...), db:Session = Depends(get_db)):
    new_tenant=create_Tenant(db=db, name=payload.name)
    return new_tenant
