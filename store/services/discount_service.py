from typing import Optional, Tuple
import random
import string
from decimal import Decimal
from ..data import discount_codes
from ..config import DISCOUNT_ORDER_INTERVAL, DISCOUNT_PERCENTAGE

def should_generate_discount(order_count: int) -> bool:
    """
    Determine if a discount code should be generated based on order count
    """
    return order_count % DISCOUNT_ORDER_INTERVAL == 0

def generate_discount_code() -> dict:
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    discount_code = {
        "code": code,
        "is_used": False,
        "order_number": len(discount_codes) + 1
    }
    discount_codes.append(discount_code)
    return discount_code

def validate_discount_code(code: str) -> dict:
    discount = next(
        (dc for dc in discount_codes if dc["code"] == code and not dc["is_used"]),
        None
    )
    return {
        "valid": bool(discount),
        "discount_percentage": DISCOUNT_PERCENTAGE if discount else 0
    }

def mark_discount_code_as_used(code: str) -> bool:
    for dc in discount_codes:
        if dc["code"] == code and not dc["is_used"]:
            dc["is_used"] = True
            return True
    return False

def calculate_discount(total: Decimal, code: Optional[str]) -> Tuple[Decimal, Optional[str]]:
    if not code:
        return Decimal('0'), None

    validation = validate_discount_code(code)
    if not validation["valid"]:
        return Decimal('0'), "Invalid or already used discount code"

    return (total * Decimal(str(validation["discount_percentage"])) / Decimal('100')), None