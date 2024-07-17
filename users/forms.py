from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User

class UserRegisterForm(UserCreationForm):
	username = forms.CharField(label='Username', widget=forms.TextInput(attrs={"class":"form-control", 'placeholder':'Username'}))
	email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={"class":"form-control", 'placeholder':'Email'})) 
	password1 = forms.CharField(label='Enter Password', widget=forms.PasswordInput(attrs={"class":"form-control", 'placeholder':'Password'}))
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control", 'placeholder':'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]
		
	