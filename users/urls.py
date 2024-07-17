from django.urls import path
from users import views

urlpatterns = [
	path('register/', views.RegisterView, name="register"),
	path('login/', views.LoginView, name="login"),
	path('logout/', views.LogoutView, name="logout"),
]