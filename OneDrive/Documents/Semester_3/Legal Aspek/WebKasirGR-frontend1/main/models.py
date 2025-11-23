from django.db import models
from django.contrib.auth.models import User

class Merchant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)

# Create your models here.
