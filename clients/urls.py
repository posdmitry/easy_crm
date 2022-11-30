from django.urls import path
from .views import MainPageView


app_name = 'clients'

urlpatterns = [
    path('', MainPageView.as_view())
]
