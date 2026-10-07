from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from ..infrastructure.database.connection import get_db
from ..infrastructure.database.models.supplier import Supplier

router = APIRouter(tags=["Suppliers"])

class ContractResponse(BaseModel):
    id: str
    name: str
    type: str
    terms: str

class SupplierResponse(BaseModel):
    id: str
    name: str
    type: str
    contactEmail: str

@router.get("/contracts", response_model=List[ContractResponse])
def get_contracts():
    return [
        ContractResponse(id="ct-1", name="Contract 1", type="manufacturer", terms="payment"),
        ContractResponse(id="ct-2", name="Contract 2", type="wholesaler", terms="payment"),
        ContractResponse(id="ct-3", name="Contract 3", type="distributor", terms="payment"),
        ContractResponse(id="ct-4", name="Contract 4", type="local_producer", terms="payment"),
    ]

@router.get("/suppliers", response_model=List[SupplierResponse])
def get_suppliers(db: Session = Depends(get_db)):
    try:
        db_suppliers = db.query(Supplier).filter(Supplier.is_active == True).all()
        if db_suppliers:
            return [
                SupplierResponse(
                    id=str(s.supplier_id),
                    name=s.supplier_name,
                    type="manufacturer",
                    contactEmail=s.email or "",
                )
                for s in db_suppliers
            ]
    except Exception:
        pass

    return [
        SupplierResponse(id="s-1", name="Luzon Meat Packers", type="manufacturer", contactEmail="orders@luzonmeat.ph"),
        SupplierResponse(id="s-2", name="Metro Dairy Wholesale", type="wholesaler", contactEmail="sales@metrodairy.ph"),
        SupplierResponse(id="s-3", name="Visayas Beverage Distributors", type="distributor", contactEmail="supply@vbd.ph"),
    ]
