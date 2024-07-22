from django.urls import path
from . import views
urlpatterns = [
    path('', views.reload, name = "get_states"),
]
