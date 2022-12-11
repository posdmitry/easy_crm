from django.urls import path
from .views import MessagesViewSet, ClientsViewSet, MessagesCreateView


app_name = 'clients_api'
API_VERSION_1 = 'v1'

urlpatterns = [
    path(f'{API_VERSION_1}/clients/', ClientsViewSet.as_view({'get': 'list'})),
    path(f'{API_VERSION_1}/clients/<int:pk>/', ClientsViewSet.as_view({'get': 'retrieve'})),
    path(f'{API_VERSION_1}/messages/', MessagesViewSet.as_view({'get': 'list'})),
    path(f'{API_VERSION_1}/messages/create/', MessagesViewSet.as_view({'post': 'create'})),
]
