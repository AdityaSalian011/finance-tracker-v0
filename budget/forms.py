from django import forms
from .models import AddBudget


class AddBudgetForm(forms.ModelForm):
    class Meta:
        model = AddBudget
        exclude = ['user', 'date']

        