from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.orm import Session

from ..infrastructure.database.connection import get_db

router = APIRouter(tags=["Auth"])

class LoginRequest(BaseModel):
    employeeId: str
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    role: str

@router.post("/auth/login", response_model=UserResponse)
def login(payload: LoginRequest):
    return UserResponse(
        id=payload.employeeId if payload.employeeId else "EMP-94822",
        name="Juan Tamad",
        role="Product Lister"
    )

@router.post("/auth/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.api_route("/me", methods=["GET", "POST"], response_model=UserResponse)
def get_current_user():
    return UserResponse(
        id="EMP-94822",
        name="Juan Tamad",
        role="Product Lister"
    )

@router.get("/fiscal-years", response_model=List[int])
def get_fiscal_years():
    return [2023, 2024, 2025, 2026]
