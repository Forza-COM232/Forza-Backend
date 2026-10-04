from enum import Enum

class PurchaseOrderStatusEnum(Enum):
    PENDING = "pending"
    RECEIVED = "received"
    COMPLETED = "completed"
    CANCELLED = "cancelled"