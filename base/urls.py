from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('frontend/',include('frontend.urls')),
    path('lgd/', include('lgd.urls')),
    path('', include('strategicbi.urls')),
    # path('agg/', include('aggrigations.urls')),
] 
