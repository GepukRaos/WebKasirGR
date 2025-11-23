from django.db import models
from django.contrib.auth.models import User
from main.models import Merchant
from menu.models import Menu

class Order(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    order_type = models.CharField(max_length=20, choices=[
        ('dine_in', 'Makan di Tempat'),
        ('takeaway','Bungkus')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name} - {self.get_order_type_display()}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.menu.name} ({self.quantity})"
