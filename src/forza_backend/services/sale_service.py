from sqlalchemy.orm import Session
from uuid import UUID
from decimal import Decimal
from ..infrastructure.database.models.sale import Sale
from ..infrastructure.database.models.sale_item import SaleItem
from ..infrastructure.database.sale_item_database import SaleItemDatabase
from ..infrastructure.database.sale_database import SaleDatabase
from ..infrastructure.database.user_database import UserDatabase
from ..infrastructure.database.product_database import ProductDatabase
from .inventory_services import InventoryService
from .stock_movement_service import StockMovementService
from ..schemas.sale import SaleCreate
from ..core.exceptions import UserAlreadyDeactivatedException, InsufficientStockException, InvalidSaleException

class SaleService:
    @staticmethod
    def create_sale(
        db: Session,
        sold_by: UUID,
        sale_data: SaleCreate
    ) -> Sale:

        if not sale_data.items:
            raise InvalidSaleException("A sale must contain at least one item.")

        user = UserDatabase.get_user_by_id(
            db,
            sold_by
        )

        if not user.is_active:
            raise UserAlreadyDeactivatedException(
                "Inactive user cannot create a sale."
            )

        sale = Sale(
            sold_by=user.user_id,
            payment_method=sale_data.payment_method
        )

        db.add(sale)
        db.flush()

        total_amount = Decimal("0.00")

        for item_data in sale_data.items:
            product = ProductDatabase.get_product(db, item_data.product_id)
            inventory = InventoryService.get_inventory_by_product(db, product.product_id)

            if inventory.quantity_on_hand < item_data.quantity:
                raise InsufficientStockException(f"Insufficient stock for {product.product_name}.")

            unit_price = product.selling_price
            item_total = unit_price * item_data.quantity            

            sale_item = SaleItem(
                sale_id=sale.sale_id,
                product_id=product.product_id,
                quantity=item_data.quantity,
                unit_price=unit_price,
                total_price=item_total
            )

            SaleItemDatabase.create_sale_item(db, sale_item)

            InventoryService.decrease_stock(
                db,
                product_id=product.product_id,
                quantity=item_data.quantity
            )

            StockMovementService.create_stock_out(
                db,
                product_id=product.product_id,
                performed_by=sold_by,
                quantity=item_data.quantity,
                reason=f"Sale {sale.sale_id}"
            )

            total_amount += item_total

        sale.total_amount = total_amount

        return SaleDatabase.create_sale(
            db,
            sale
        )