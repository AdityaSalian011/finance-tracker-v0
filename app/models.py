from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class AddExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    EXP_CAT_OPTIONS = [
        ('food', 'Food'),
        ('rent', 'Rent'),
        ('entertainment', 'Entertainment'),
        ('other', 'Other'),
    ]
    exp_category = models.CharField(max_length=13, choices=EXP_CAT_OPTIONS, default='food')

    name = models.CharField(max_length=50, blank=True, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    comment = models.CharField(max_length=255, blank=True, null=True)

    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.exp_category} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.name and self.name.strip().lower() == 'none':
            self.name = None
        elif self.name and not self.name.strip():  # " " ""
            self.name = None

        super().save(*args, **kwargs)