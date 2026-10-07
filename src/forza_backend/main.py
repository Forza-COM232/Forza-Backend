from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, dashboard, analytics, suppliers, landing, categories, sample

app = FastAPI(
    title="Forza Backend API",
    description="Backend API for Forza Inventory & Supply Chain Management",
    version="1.0.0"
)

# Enable CORS for the frontend Vite / React dev servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
def startup_event():
    try:
        from .infrastructure.database.connection import Base, engine
        from .infrastructure.database.models import (
            category, product, inventory, supplier, purchase_order,
            purchase_order_item, sale, sale_item, stock_movement, users
        )
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print("Database startup notice:", e)

# API Router with /api prefix (matches frontend VITE_API_URL default)
api_router = APIRouter(prefix="/api")

routers = [
    auth.router,
    dashboard.router,
    analytics.router,
    suppliers.router,
    landing.router,
    categories.router,
    sample.router,
]

for r in routers:
    api_router.include_router(r)
    # Also include at root level so both /api/... and /... work seamlessly
    app.include_router(r)

app.include_router(api_router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Forza Backend is running"}
