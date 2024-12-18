from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product-list'),
    path('cart/checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('discount/validate/', views.ValidateDiscountView.as_view(), name='validate-discount'),
    path('admin/stats/', views.AdminStatsView.as_view(), name='admin-stats'),
]