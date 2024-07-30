from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('frontend.urls')),
    path('lgd/', include('lgd.urls')),
    path('bi/', include('strategicbi.urls')),
] 
