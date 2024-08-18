from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms

# class RegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
    
#     class Meta:
#         model = User
#         fields = ['username' , 'email', 'password1', 'password2']

class RegistrationForm(UserCreationForm):
    ''' sign up form'''
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class CustomLoginForm(AuthenticationForm):
    '''login form'''
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'password'}))
