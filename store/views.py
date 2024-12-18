"""
API views for the store application
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Dict, Any

from .services.product_service import get_all_products
from .services.order_service import create_order, get_order_stats
from .services.discount_service import validate_discount_code, generate_discount_code

class ProductList(APIView):
    def get(self, request) -> Response:
        products = get_all_products()
        return Response(products)

class CheckoutView(APIView):
    def post(self, request) -> Response:
        order, should_generate_discount, error = create_order(request.data)
        
        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        response_data: Dict[str, Any] = {"order": order}
        
        if should_generate_discount:
            discount = generate_discount_code()
            response_data["discount_code"] = discount["code"]
        
        return Response(response_data, status=status.HTTP_201_CREATED)

class ValidateDiscountView(APIView):
    def post(self, request) -> Response:
        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "No discount code provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = validate_discount_code(code)
        return Response(result)

class AdminStatsView(APIView):
    def get(self, request) -> Response:
        stats = get_order_stats()
        return Response(stats)