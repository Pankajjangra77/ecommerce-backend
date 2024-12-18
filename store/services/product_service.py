from typing import List, Dict, Any, Optional
from ..data import products

def get_all_products() -> List[Dict[str, Any]]:
    return products

def get_product_by_id(product_id: int) -> Optional[Dict[str, Any]]:
    return next((product for product in products if product["id"] == product_id), None)