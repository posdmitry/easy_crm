from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clients.urls', namespace='clients')),
    path('api/', include('clients_api.urls', namespace='clients_api')),
]
