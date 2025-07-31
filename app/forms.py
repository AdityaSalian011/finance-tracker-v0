from django import forms
from .models import AddExpense


class AddExpenseForm(forms.ModelForm):
    class Meta:
        model = AddExpense
        exclude = ['user', 'date']