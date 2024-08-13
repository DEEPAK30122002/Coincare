from django.urls import path
from . import views
from .views import base_view

urlpatterns = [
    path('', views.index,name="expenses"),
    path('add-expense', views.add_expense,name="expenses"),
    path('base/', base_view, name='base'),
]
