from bdb import effective
from unicodedata import name
from django.db import models

# Create your models here.

class Dealer(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    cr_limit = models.IntegerField()
    balance = models.IntegerField()
    territory = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    product =models.CharField(max_length=30)
    p_name =models.CharField(max_length=100)
    UOM = models.CharField(max_length=10)
    tp = models.IntegerField()

    def __str__(self):
        return self.p_name

class Promotion(models.Model):
    id = models.AutoField(primary_key=True)
    p_code = models.CharField(max_length=10)
    p_name = models.CharField(max_length=100)
    UOM = models.CharField(max_length=10)
    order_qty = models.IntegerField()
    bonus_qty = models.IntegerField()
    status = models.IntegerField()
    sdp = models.CharField(max_length=50)
    region = models.CharField(max_length=20)
    territory =models.CharField(max_length= 20)
    remarks =models.CharField(max_length=300)
    effective_date =models.DateField()
    entry_date = models.DateField()

    def __str__(self):
        return self.sdp

class order(models.Model):
    id = models.AutoField(primary_key=True)
    product =models.CharField(max_length=30)
    p_name =models.CharField(max_length=100)
    UOM = models.CharField(max_length=10)
    tp = models.IntegerField()
    order_qty = models.IntegerField()
    bonus_qty = models.IntegerField()
    balance = models.IntegerField()

    def __str__(self):
        return self.p_name

