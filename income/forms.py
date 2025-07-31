from .models import AddIncome
from django import forms


class AddIncomeForm(forms.ModelForm):
    class Meta:
        model = AddIncome
        exclude = ['user', 'date']

