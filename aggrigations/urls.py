from django.urls import path
from . import views
urlpatterns = [
    path('places/', views.load_places, name = "get_states"),
    path('places/state', views.load_place_state, name = 'state_place'),
    path('places/district', views.load_place_district, name = 'district_place'),
    path('places/subdistrict', views.load_place_subdistrict, name = 'subdistrict_place'),
    path('places/village', views.load_place_village, name = 'village_place'),
    path('places/state/avg-rating', views.get_total_user_ratings, name = 'avg-rating-state'),
    
]
