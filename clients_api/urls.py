from django.urls import path
from .views import ClientsList, ClientDetail


app_name = 'clients_api'

urlpatterns = [
    path('', ClientsList.as_view(), name='listcreate'),
    path('<int:pk>/', ClientDetail.as_view(), name='detailcreate')
]
