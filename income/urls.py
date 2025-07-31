from django.urls import path 
from . import views

urlpatterns = [
    path('', views.addIncome, name='add_income'),
    path('show', views.showIncome, name='show_income'),
    path('edit/<int:entry_id>', views.editIncome, name='edit_income'),
    path('download', views.download_income, name='download_income')
]