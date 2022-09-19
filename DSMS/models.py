
from datetime import datetime
from io import BufferedRandom
from django.db import models

# Create your models here.
 
class Product(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    product_name = models.CharField(max_length=50)
    product_id = models.CharField(max_length=20)
    product_quantity = models.IntegerField(null=True)
    brand = models.CharField(max_length=50, default='N/A')

class Orders(models.Model):
    product_name = models.CharField(max_length=50)
    product_quantity = models.IntegerField(null=False, default=1)
    ordered = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    username = models.CharField(max_length=50)
    order_id = models.CharField(max_length=50)
    date = models.DateField()

class Approvals(models.Model):
    product_name = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    product_quantity = models.IntegerField(null=False, default=1)
    approved = models.BooleanField("Approved",default=False)
    date = models.DateField()
