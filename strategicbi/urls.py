from django.urls import path
from . import views

urlpatterns = [
    # path('get-json/', views.get_json, name = "get-json"),
    # path('home/', views.home, name = "home"),
    path('send-json/', views.send_json_response, name='send-json'),
    path('fetch/', views.fetch_screen, name = "fetch"),
    path('fetch-message/', views.fetch_message, name = "fetch-message"),
    path('fetch-function/', views.fetch_function, name = "fetch-function"),
    path('display/', views.display_view, name='display'),
    path('display/get_details/', views.get_details, name='get_details'),
    path('display/get_process_time_details/', views.get_processing_time_details, name='get_process_time_details'),
    path('display/<int:catagory>/', views.display_view, name='display_view'),
    path('display/download-csv/', views.download_csv, name='download-csv'),
    # path("view-all/",views.view_all, name="view-all"),
    path('home/load-districts/', views.load_districts, name='load_districts'),
    path('fetch/load-districts/', views.load_districts, name='load_districts'),
    # path('load-subdistricts/', views.load_subdistricts, name='load_subdistricts'),
    # path('load-villages/', views.load_villages, name='load_villages'),
]
