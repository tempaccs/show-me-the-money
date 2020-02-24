from django.db import models
from customers.models import Customer

class Flow(models.TextChoices):
    OUTFLOW = 'outflow', 'outflow'
    INFLOW = 'inflow', 'inflow'

class Category(models.TextChoices):
    GROCERIES = 'groceries', 'groceries'
    SALARY = '"salary",', '"salary",'
    TRANSFER = 'transfer', 'transfer'
    RENT = 'rent', 'rent'
    SAVINGS = 'savings', 'savings'
    OTHER = 'other', 'other'

class Transaction(models.Model):
    reference = models.CharField(max_length=10, unique=True)
    account = models.CharField(max_length=10)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(choices=Flow.choices, max_length=20)
    category = models.CharField(choices=Category.choices, max_length=20)
    user = models.ForeignKey(Customer, on_delete=models.PROTECT)