from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                 redirect_authenticated_user=True), name='login'),
    path('signup/', views.sign_up, name = "signup"),
    path('', include('django.contrib.auth.urls')),
]