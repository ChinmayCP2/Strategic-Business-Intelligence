from django.shortcuts import render, redirect
import logging
from .forms import RegistrationForm
from django.contrib.auth import login
# Create your views here.

def sign_up(request):
    '''Sign Up with a custom form'''
    if request.method == "POST":
        logging.info("registration form submitted")
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logging.info("registration form accepted")
            login(request, user)
            return redirect('auth/home')
    else:
        logging.info("registration form displayed")
        form =  RegistrationForm()
    return render(request, "registration/signup.html", {"form" : form})
