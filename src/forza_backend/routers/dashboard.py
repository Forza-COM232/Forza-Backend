from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from ..infrastructure.database.connection import get_db
from ..infrastructure.database.models.product import Product
from ..infrastructure.database.models.inventory import Inventory
from ..infrastructure.database.models.sale import Sale

router = APIRouter(tags=["Dashboard"])

class SalesMetric(BaseModel):
    count: int
    changePercent: float

class RevenueMetric(BaseModel):
    amount: float
    changePercent: float

class DashboardSummaryResponse(BaseModel):
    totalProducts: int
    sales: SalesMetric
    revenue: RevenueMetric
    alerts: int

class SupplyChannelResponse(BaseModel):
    id: str
    name: str
    type: str
    status: str

class LowStockProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    quantity: int
    reorderLevel: int

class BreakdownMetric(BaseModel):
    turnover: int
    daysSales: int

class InventoryHealthResponse(BaseModel):
    accumulatePercent: int
    breakdown: BreakdownMetric
    targetPercent: int
    turnoverRate: int
    daysSalesOfInventory: int
    reorderAlerts: int
    defectRate: int

class AverageSalesResponse(BaseModel):
    percent: float

@router.get("/dashboard/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(year: Optional[int] = Query(None), db: Session = Depends(get_db)):
    try:
        total_products = db.query(Product).count()
        alerts = db.query(Inventory).join(Product).filter(Inventory.quantity_on_hand <= Product.reorder_level).count()
        if total_products > 0:
            return DashboardSummaryResponse(
                totalProducts=total_products,
                sales=SalesMetric(count=500_000, changePercent=-0.5),
                revenue=RevenueMetric(amount=37_953_458.0, changePercent=-1.7),
                alerts=alerts
            )
    except Exception:
        pass

    return DashboardSummaryResponse(
        totalProducts=310,
        sales=SalesMetric(count=500_000, changePercent=-0.5),
        revenue=RevenueMetric(amount=37_953_458.0, changePercent=-1.7),
        alerts=4
    )

@router.get("/supply-channels", response_model=List[SupplyChannelResponse])
def get_supply_channels():
    return [
        SupplyChannelResponse(id="sc-1", name="Manufacturer", type="manufacturer", status="On-Site"),
        SupplyChannelResponse(id="sc-2", name="Wholesalers", type="wholesaler", status="On-Site"),
        SupplyChannelResponse(id="sc-3", name="Distributors", type="distributor", status="On-Site"),
        SupplyChannelResponse(id="sc-4", name="Local Producers", type="local_producer", status="On-Site"),
    ]

@router.get("/products/low-stock", response_model=List[LowStockProductResponse])
def get_low_stock_products(db: Session = Depends(get_db)):
    try:
        low_stocks = (
            db.query(Product, Inventory)
            .join(Inventory, Product.product_id == Inventory.product_id)
            .filter(Inventory.quantity_on_hand <= Product.reorder_level)
            .limit(10)
            .all()
        )
        if low_stocks:
            return [
                LowStockProductResponse(
                    id=str(p.product_id),
                    name=p.product_name,
                    sku=p.sku,
                    quantity=inv.quantity_on_hand,
                    reorderLevel=p.reorder_level,
                )
                for p, inv in low_stocks
            ]
    except Exception:
        pass

    return [
        LowStockProductResponse(id="p-1", name="Ribeye Steak 500g", sku="MEAT-0142", quantity=6, reorderLevel=20),
        LowStockProductResponse(id="p-2", name="Salted Butter 113g", sku="DAIRY-0088", quantity=12, reorderLevel=40),
        LowStockProductResponse(id="p-3", name="Cola Can 330ml", sku="BEV-0310", quantity=18, reorderLevel=60),
        LowStockProductResponse(id="p-4", name="Extra Virgin Olive Oil 1L", sku="PANTRY-0217", quantity=4, reorderLevel=15),
        LowStockProductResponse(id="p-5", name="Organic Rice Pilaf", sku="PANTRY-0233", quantity=9, reorderLevel=25),
    ]

@router.get("/inventory/health", response_model=InventoryHealthResponse)
def get_inventory_health():
    return InventoryHealthResponse(
        accumulatePercent=78,
        breakdown=BreakdownMetric(turnover=39, daysSales=22),
        targetPercent=85,
        turnoverRate=555,
        daysSalesOfInventory=9,
        reorderAlerts=1548,
        defectRate=88,
    )

@router.get("/sales/average", response_model=AverageSalesResponse)
def get_average_sales(year: Optional[int] = Query(None)):
    return AverageSalesResponse(percent=77.77)

@router.get("/inventory/updates", response_model=List[List[int]])
def get_inventory_updates():
    heat_sequence = [3, 0, 0, 2, 0, 3, 2, 1, 0, 2, 3, 0, 2, 0, 1, 3, 0, 0, 2, 0, 3]
    return [heat_sequence[row:row + 18] for row in range(4)]
