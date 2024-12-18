from typing import Tuple, Optional, Dict, Any
import uuid
from decimal import Decimal
from ..data import orders, discount_codes
from .discount_service import (
    calculate_discount,
    mark_discount_code_as_used,
    should_generate_discount
)

def create_order(order_data: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], bool, Optional[str]]:
    """
    Returns tuple of (order, should_generate_discount, error_message)
    """
    try:
        order_id = str(uuid.uuid4())[:10]
        total = Decimal(str(order_data["total"]))
        discount_code = order_data.get("discount_code")
        
        discount_amount, error = calculate_discount(total, discount_code)
        if error:
            return None, False, error
            
        if discount_code and discount_amount > 0:
            if not mark_discount_code_as_used(discount_code):
                return None, False, "Failed to apply discount code"
        
        final_total = total - discount_amount
        
        order = {
            "order_id": order_id,
            "items": order_data["items"],
            "total": float(total),
            "discount_code": discount_code,
            "discount_amount": float(discount_amount),
            "final_total": float(final_total),
        }
        
        orders.append(order)
        generate_discount = should_generate_discount(len(orders))
        
        return order, generate_discount, None
        
    except Exception as e:
        return None, False, str(e)

def get_order_stats() -> Dict[str, Any]:
    total_items = sum(
        sum(item["quantity"] for item in order["items"])
        for order in orders
    )
    
    total_amount = sum(Decimal(str(order["total"])) for order in orders)
    total_discount = sum(Decimal(str(order["discount_amount"])) for order in orders)
    
    return {
        "total_items_purchased": total_items,
        "total_purchase_amount": float(total_amount),
        "total_discount_amount": float(total_discount),
        "discount_codes": [
            {
                "code": dc["code"],
                "is_used": dc["is_used"],
                "order_number": dc["order_number"]
            }
            for dc in discount_codes
        ]
    }