from django.shortcuts import render, redirect
import logging
from .forms import RegistrationForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from django.contrib import messages

# Create your views here.

logger = logging.getLogger('auth_app')

class CustomLoginView(auth_views.LoginView):
    '''login page'''
    form_class = CustomLoginForm
    template_name = 'registration/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome back, {self.request.user.username}!')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

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
