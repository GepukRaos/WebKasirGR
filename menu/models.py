from django.db import models
from main.models import Merchant

class Menu(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name="menus")
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.name} - Rp{self.price}"
