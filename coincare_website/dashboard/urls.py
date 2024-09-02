from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expenses-summary/', views.expense_summary, name='expense_summary'),
    path('income-summary/', views.income_summary, name='income_summary'),
    path('balance-summary/', views.balance_summary, name='balance_summary'),
]