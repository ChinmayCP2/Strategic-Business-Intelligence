from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('get-json/', views.get_json, name = "get-json"),
    path('home/', views.home, name = "home"),
    path('send-json/', views.send_json_response, name='send-json'),
    path('fetch/', views.fetch_screen, name = "fetch"),
    path('fetch-message/', views.fetch_message, name = "fetch-message"),
    path('fetch-function/', views.fetch_function, name = "fetch-function"),
    path('display/', views.display_view, name='display'),
    path('get_details/', views.get_details, name='get_details'),
    path('display/<int:catagory>/', views.display_view, name='display_view'),
    # path("view-all/",views.view_all, name="view-all"),
    path('load-districts/', views.load_districts, name='load_districts'),
    # path('load-subdistricts/', views.load_subdistricts, name='load_subdistricts'),
    # path('load-villages/', views.load_villages, name='load_villages'),
    path('', include('django.contrib.auth.urls')),
]
