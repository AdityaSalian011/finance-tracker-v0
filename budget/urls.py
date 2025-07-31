from django.urls import path
from . import views


urlpatterns = [
    path('', views.addBudget, name='add_budget'),
    path('edit/<int:entry_id>', views.editBudget, name='edit_budget'),
    path('delete/<int:entry_id>', views.deleteBudget, name='delete_budget'),
    path('download', views.download_budget, name='download_budget'),
]