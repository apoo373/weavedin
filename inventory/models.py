# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    Name = models.CharField(max_length=200)
    Brand = models.CharField(max_length=200)
    Category = models.CharField(max_length=200)
    ProductCode = models.CharField(max_length=200)

class Variant(models.Model):
    Name = models.CharField(max_length=200)
    CostPrice = models.FloatField()
    SellingPrice = models.FloatField()
    Quantity = models.IntegerField(default=0)
    Item = models.ForeignKey(Item, on_delete=None)

class Property(models.Model):
    Name = models.CharField(max_length=200)
    Value = models.CharField(max_length=200)
    Variant = models.ForeignKey(Variant, on_delete=None)

class InventoryLog(models.Model):
    time = models.DateTimeField(auto_now_add=True, editable=False, null=False, blank=False)
    user = models.ForeignKey(User)
    content = models.TextField(blank=True)
