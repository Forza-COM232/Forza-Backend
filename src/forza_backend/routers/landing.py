from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(tags=["Landing"])

class RegionPerformanceResponse(BaseModel):
    id: str
    region: str
    foodSegments: int

class LandingStatResponse(BaseModel):
    id: str
    percent: float
    label: str

@router.get("/store-performance", response_model=List[RegionPerformanceResponse])
def get_store_performance():
    return [
        RegionPerformanceResponse(id="r-1", region="Metro Manila Core", foodSegments=410),
        RegionPerformanceResponse(id="r-2", region="Luzon Provinces", foodSegments=308),
        RegionPerformanceResponse(id="r-3", region="Visayas & Mindanao", foodSegments=81),
    ]

@router.get("/landing/stats", response_model=List[LandingStatResponse])
def get_landing_stats():
    return [
        LandingStatResponse(id="ls-1", percent=84.0, label="Reduction in manual PO drafting time"),
        LandingStatResponse(id="ls-2", percent=-30.0, label="Lower warehouse carrying costs"),
    ]
