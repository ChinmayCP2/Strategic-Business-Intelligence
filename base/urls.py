from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('frontend/',include('frontend.urls')),
    path('lgd/', include('lgd.urls')),
    path('bi/', include('strategicbi.urls')),
    path('', include('auth_app.urls')),
    # path('agg/', include('aggrigations.urls')),
] + debug_toolbar_urls()
