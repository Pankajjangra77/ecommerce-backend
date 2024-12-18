from django.db import models
import random
import string

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    order_id = models.CharField(max_length=10, unique=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount_code = models.CharField(max_length=20, null=True, blank=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    order_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def generate_code(cls):
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choices(chars, k=8))

    def __str__(self):
        return self.code