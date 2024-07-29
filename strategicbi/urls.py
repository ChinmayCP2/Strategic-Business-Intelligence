from django.urls import path
from . import views

urlpatterns = [
    path('get-json/', views.get_json, name = "get-json"),
    path('extract-json/', views.extract_json, name = "extract-json"),
    path('send-json/', views.send_json_response, name = "send-json"),
]
