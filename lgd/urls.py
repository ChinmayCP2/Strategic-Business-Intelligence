from django.urls import path
from . import views
urlpatterns = [
    path('state/', views.load_state, name = "get_states"),
    path('dist/', views.load_district, name = "get_districts"),
    path('subdist/', views.load_sub_district, name = "get_districts"),
    path('village/', views.load_village, name = "get_village"),
    path('<str:region>/reset/', views.reset_db, name = "reset_db"),
]
