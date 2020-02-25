from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Customer(models.Model):
    name = models.CharField(max_length=60)
    email = models.EmailField()
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(16), MaxValueValidator(120)]
    )
