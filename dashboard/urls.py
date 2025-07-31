from django.urls import path
from . import views

urlpatterns = [
    path('', views.getDashboardInfo, name='dashboard'),
]