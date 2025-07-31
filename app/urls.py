from django.urls import path 
from . import views

urlpatterns = [
    path('', views.addExpense, name='add_expense'),
    path('delete/<int:entry_id>', views.deleteExpense, name='delete_expense'),
    path('edit/<int:entry_id>', views.editExpense, name='edit_expense'),
    path('download', views.download_expense, name='download_expense')
]