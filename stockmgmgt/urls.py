from django.urls import path 
from . import views

urlpatterns = [
	path('', views.home, name='home'),
    path('list_item/', views.list_item, name='list_item'),
]