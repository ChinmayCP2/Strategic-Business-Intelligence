from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('get-json/', views.get_json, name = "get-json"),
    # path('extract-json/', views.extract_json, name = "extract-json"),
    path('send-json/', views.send_json_response, name='send-json'),
    path('', views.home, name = "home"),
    path('display/', views.display_view, name='display_view'),
    path('get_details/', views.get_details, name='get_details'),
    path('display/<int:catagory>/', views.display_view, name='display_view'),
    # path("view-all/",views.view_all, name="view-all"),
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html",
                                                 redirect_authenticated_user=True), name='login'),
    path('signup/', views.sign_up, name = "signup"),
    path('load-districts/', views.load_districts, name='load_districts'),
    # path('load-subdistricts/', views.load_subdistricts, name='load_subdistricts'),
    # path('load-villages/', views.load_villages, name='load_villages'),
    path('', include('django.contrib.auth.urls')),
]
