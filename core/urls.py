from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clients.urls', namespace='clients')),
    path('api/', include('clients_api.urls', namespace='clients_api')),

    # JWT auth
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/verify/', TokenVerifyView.as_view()),

    re_path(r'^auth/', include('djoser.urls'))
]
