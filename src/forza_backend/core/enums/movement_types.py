from enum import Enum

class MovementType(str, Enum):
    STOCK_IN = "stock_in"
    STOCK_OUT = "stock_out"
    SALE = "sale"
    RETURN = "return"
    DAMAGE = "damage"
    EXPIRED = "expired"
    ADJUSTMENT = "adjustment"
