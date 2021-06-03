from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list_items/', views.list_items, name='list_item'),
    path('add_items/', views.add_items, name='add_item'),
]
