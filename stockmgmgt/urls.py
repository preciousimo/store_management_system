from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('list_item/', views.list_items, name='list_item'),
    path('add_item/', views.add_items, name='add_item'),
]
