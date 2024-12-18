"""
Unit tests for store services
"""
from django.test import TestCase
from decimal import Decimal
from store.services.discount_service import (
    validate_discount_code,
    calculate_discount,
    generate_discount_code
)
from store.services.order_service import create_order, get_order_stats
from store.services.product_service import get_all_products, get_product_by_id
from store.data import products, orders, discount_codes

class TestDiscountService(TestCase):
    def setUp(self):
        discount_codes.clear()
        orders.clear()

    def test_generate_discount_code(self):
        """Test discount code generation"""
        code = generate_discount_code()
        self.assertIsNotNone(code["code"])
        self.assertEqual(len(code["code"]), 8)
        self.assertFalse(code["is_used"])
        self.assertEqual(code["order_number"], 1)

    def test_validate_discount_code(self):
        """Test discount code validation"""
        code = generate_discount_code()
        
        result = validate_discount_code(code["code"])
        self.assertTrue(result["valid"])
        self.assertEqual(result["discount_percentage"], 10)
        
        result = validate_discount_code("INVALID")
        self.assertFalse(result["valid"])
        self.assertEqual(result["discount_percentage"], 0)

    def test_calculate_discount(self):
        """Test discount calculation"""
        code = generate_discount_code()
        
        amount, error = calculate_discount(Decimal('100'), code["code"])
        self.assertEqual(amount, Decimal('10'))
        self.assertIsNone(error)
        
        amount, error = calculate_discount(Decimal('100'), "INVALID")
        self.assertEqual(amount, Decimal('0'))
        self.assertIsNotNone(error)

class TestOrderService(TestCase):
    def setUp(self):
        orders.clear()
        discount_codes.clear()

    def test_create_order(self):
        order_data = {
            "items": [
                {"product": 1, "quantity": 2, "price": 199.99}
            ],
            "total": "399.98",
            "discount_code": None,
            "discount_amount": "0",
            "final_total": "399.98"
        }
        
        order, should_generate, error = create_order(order_data)
        
        self.assertIsNotNone(order)
        self.assertIsNone(error)
        self.assertFalse(should_generate)
        self.assertEqual(len(orders), 1)

    def test_get_order_stats(self):
        order_data = {
            "items": [
                {"product": 1, "quantity": 2, "price": 199.99}
            ],
            "total": "399.98",
            "discount_code": None,
            "discount_amount": "0",
            "final_total": "399.98"
        }
        
        create_order(order_data)
        create_order(order_data)
        
        stats = get_order_stats()
        
        self.assertEqual(stats["total_items_purchased"], 4)
        self.assertAlmostEqual(float(stats["total_purchase_amount"]), 799.96, places=2)
        self.assertEqual(float(stats["total_discount_amount"]), 0)

class TestProductService(TestCase):
    def test_get_all_products(self):
        all_products = get_all_products()
        self.assertEqual(len(all_products), len(products))
        self.assertEqual(all_products[0]["name"], "Premium Wireless Headphones")

    def test_get_product_by_id(self):
        product = get_product_by_id(1)
        self.assertIsNotNone(product)
        self.assertEqual(product["name"], "Premium Wireless Headphones")
        
        product = get_product_by_id(999)
        self.assertIsNone(product)