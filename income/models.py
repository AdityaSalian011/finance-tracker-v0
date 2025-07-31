from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class AddIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2, default=0,
    validators=[MinValueValidator(0)]
    )
    business_income = models.DecimalField(max_digits=10, decimal_places=2, default=0,
    validators=[MinValueValidator(0)]
    )
    freelance_income = models.DecimalField(max_digits=10, decimal_places=2, default=0,
    validators=[MinValueValidator(0)]
    )
    other_income = models.DecimalField(max_digits=10, decimal_places=2, default=0,
    validators=[MinValueValidator(0)]
    )

    date = models.DateField(default=timezone.now())