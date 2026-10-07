from fastapi import APIRouter, Query
from typing import Optional, Dict, Any, List

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/inventory-turnover")
def get_inventory_turnover(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "turnoverRate": 555, "ratio": 4.2}

@router.get("/gross-margin")
def get_gross_margin(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "marginPercent": 32.5}

@router.get("/lead-time")
def get_lead_time(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "averageLeadTimeDays": 5.4}

@router.get("/holding-cost")
def get_holding_cost(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "totalHoldingCost": 12450.00}

@router.get("/stock-movement")
def get_stock_movement() -> Dict[str, Any]:
    return {"inflow": 120, "outflow": 95, "netChange": 25}

@router.get("/demand")
def get_demand(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "forecastedGrowth": 12.8}

@router.get("/supplier-performance")
def get_supplier_performance(year: Optional[int] = Query(None)) -> Dict[str, Any]:
    return {"year": year, "onTimeRate": 94.2, "defectRate": 1.5}
