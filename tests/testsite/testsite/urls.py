from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('testapp/', include('testapp.urls')),
    path('admin/', admin.site.urls),
]