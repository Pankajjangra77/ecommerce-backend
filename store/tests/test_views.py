"""
Unit tests for store views
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from store.data import products, orders, discount_codes

class StoreViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        orders.clear()
        discount_codes.clear()

    def test_product_list(self):
        url = reverse('product-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(products))

    def test_checkout(self):
        url = reverse('checkout')
        data = {
            "items": [
                {"product": 1, "quantity": 2, "price": 199.99}
            ],
            "total": "399.98",
            "discount_code": None,
            "discount_amount": "0",
            "final_total": "399.98"
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order', response.data)
        self.assertEqual(len(orders), 1)

    def test_validate_discount(self):
        checkout_url = reverse('checkout')
        for _ in range(3): 
            data = {
                "items": [{"product": 1, "quantity": 1, "price": 199.99}],
                "total": "199.99",
                "final_total": "199.99"
            }
            self.client.post(checkout_url, data, format='json')
        
        discount_code = discount_codes[0]["code"]
        
        url = reverse('validate-discount')
        response = self.client.post(url, {"code": discount_code}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["valid"])
        self.assertEqual(response.data["discount_percentage"], 10)

    def test_admin_stats(self):
        checkout_url = reverse('checkout')
        data = {
            "items": [{"product": 1, "quantity": 2, "price": 199.99}],
            "total": "399.98",
            "final_total": "399.98"
        }
        self.client.post(checkout_url, data, format='json')
        
        url = reverse('admin-stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_items_purchased', response.data)
        self.assertIn('total_purchase_amount', response.data)
        self.assertIn('total_discount_amount', response.data)
        self.assertIn('discount_codes', response.data)