from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from ..infrastructure.database.models.purchase_order import PurchaseOrder
from ..infrastructure.database.models.purchase_order_item import PurchaseOrderItem
from ..infrastructure.database.purchase_order_database import PurchaseOrderDatabase
from ..infrastructure.database.supplier_database import SupplierDatabase
from ..infrastructure.database.user_database import UserDatabase
from ..infrastructure.database.product_database import ProductDatabase
from ..schemas.purchase import PurchaseOrderCreate, PurchaseOrderUpdate
from ..core.enums.purchase_order_status import PurchaseOrderStatusEnum
from ..core.exceptions import (
    PurchaseOrderSupplierInactiveException,
    UserAlreadyDeactivatedException,
    PurchaseOrderStatusException
)

class PurchaseOrderService():
    @staticmethod
    def get_purchase_order_by_id(db: Session, purchase_order_id: UUID) -> PurchaseOrder:
        return PurchaseOrderDatabase.get_purchase_order(db, purchase_order_id)
    
    @staticmethod
    def create_purchase_order(db: Session, purchase_order_data: PurchaseOrderCreate, order_by: UUID) -> PurchaseOrder:
        supplier = SupplierDatabase.get_supplier_by_id(db, purchase_order_data.supplier_id)
        if not supplier.is_active:
            raise PurchaseOrderSupplierInactiveException("Cannot create purchase order for inactive supplier")
        
        user = UserDatabase.get_user_by_id(db, order_by)
        if not user.is_active:
            raise UserAlreadyDeactivatedException("Inactive user cannot create a purchase order")
        
        purchase_order = PurchaseOrder(
            supplier_id=supplier.supplier_id,
            order_by=user,
            status = PurchaseOrderStatusEnum.PENDING,
            total_amount = Decimal("0.00")
        )
        
        total_amount = Decimal("0.00")
        
        for item_data in purchase_order_data.purchase_order_item:
            product = ProductDatabase.get_product(db, item_data.product_id)
            
            total_price = item_data.quantity * item_data.unit_cost
            
            purchase_item = PurchaseOrderItem(
                product_id = product.product_id,
                quantity = item_data.quantity,
                unit_cost = item_data.unit_cost,
                total_price = total_price
            )
            
            purchase_order.items.append(purchase_item)
            
            total_amount += total_price
        purchase_order.total_amount = total_amount
        
        PurchaseOrderDatabase.create_purchase_order(db, purchase_order)
        
        return purchase_order
    
    def update_purchase_order(self, db: Session, purchase_order_id: UUID, purchase_data: PurchaseOrderUpdate) -> PurchaseOrder:
        purchase_order = PurchaseOrderDatabase.get_purchase_order(db, purchase_order_id)
        if purchase_order.status != PurchaseOrderStatusEnum.PENDING:
            raise PurchaseOrderStatusException("Only purchase order with pending status can be edited")
        
        if purchase_order.status == PurchaseOrderStatusEnum.COMPLETED:
            raise PurchaseOrderStatusException("Completed purchase order cannot be modified")
        
        if purchase_data.status is not None:
            self._validate_status_transition(
                current_status=purchase_order.status,
                new_status=purchase_data.status
            )
            
            purchase_order.status = purchase_data.status
        
        return PurchaseOrderDatabase.update_purchase_order(db, purchase_order)
    
    @staticmethod
    def receive_purchase_order(db: Session, purchase_order_id: UUID) -> PurchaseOrder:
        purchase_order = PurchaseOrderDatabase.get_purchase_order(db, purchase_order_id)
        if purchase_order.status != PurchaseOrderStatusEnum.PENDING:
            raise PurchaseOrderStatusException("Only pending purchase order can be received.")
        
        for item in purchase_order.items:
            # Insert inventory service logic
            # Insert stock_movement service logic
            item = print()
        
        purchase_order.status = PurchaseOrderStatusEnum.RECEIVED
        
        return PurchaseOrderDatabase.update_purchase_order(db, purchase_order)
    
    @staticmethod
    def cancelled_purchase_order(db: Session, purchase_order_id: UUID) -> PurchaseOrder:
        purchase_order = PurchaseOrderDatabase.get_purchase_order(db, purchase_order_id)
        if purchase_order.status != PurchaseOrderStatusEnum.PENDING:
            raise PurchaseOrderStatusException("Only pending purchase order can be cancelled.")
        
        purchase_order.status = PurchaseOrderStatusEnum.CANCELLED
        
        return PurchaseOrderDatabase.update_purchase_order(db, purchase_order)
    
    def _validate_status_transition(
        self,
        current_status: PurchaseOrderStatusEnum,
        new_status: PurchaseOrderStatusEnum,
    ) -> None:
        allowed_transitions = {
            PurchaseOrderStatusEnum.PENDING: {
                PurchaseOrderStatusEnum.PENDING,
                PurchaseOrderStatusEnum.RECEIVED,
            },
            PurchaseOrderStatusEnum.RECEIVED: {
                PurchaseOrderStatusEnum.RECEIVED,
                PurchaseOrderStatusEnum.COMPLETED,
            },
            PurchaseOrderStatusEnum.COMPLETED: {
                PurchaseOrderStatusEnum.COMPLETED,
            },
        }

        if new_status not in allowed_transitions[current_status]:
            raise PurchaseOrderStatusException(
                f"Cannot change status from "
                f"{current_status.value} to {new_status.value}"
            )