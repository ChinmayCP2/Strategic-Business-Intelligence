from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name = "index"),
    path('load-districts/', views.load_districts, name='load_districts'),
    path('load-subdistricts/', views.load_subdistricts, name='load_subdistricts'),
    path('load-villages/', views.load_villages, name='load_villages'),

]
