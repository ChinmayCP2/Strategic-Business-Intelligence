from django.shortcuts import render, redirect
import logging
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm

# Create your views here.

logger = logging.getLogger('auth_app')

class CustomLoginView(auth_views.LoginView):
    '''login page'''
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

def sign_up(request):
    '''Sign Up with a custom form'''
    if request.method == "POST":
        logger.info("registration form submitted")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info("registration form accepted")
            login(request, user)
            return redirect('home')
    else:
        form =  RegistrationForm()
        logger.info("Displaying Registration form")
    return render(request, "registration/signup.html", {"form" : form})
