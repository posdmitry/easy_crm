from django.urls import path
from .views import ClientsViewSet, MessageCreateView, ClientTypesView, IndustriesView

app_name = 'clients_api'
API_VERSION_1 = 'v1'

urlpatterns = [
    # main routes
    path(f'{API_VERSION_1}/clients/', ClientsViewSet.as_view({'get': 'list'})),
    path(f'{API_VERSION_1}/clients/<int:pk>/', ClientsViewSet.as_view({'get': 'retrieve'})),
    path(f'{API_VERSION_1}/clients/create/', ClientsViewSet.as_view({'post': 'create'})),
    path(f'{API_VERSION_1}/clients/update/<int:pk>/', ClientsViewSet.as_view({'put': 'update'})),
    path(f'{API_VERSION_1}/clients/delete/<int:pk>/', ClientsViewSet.as_view({'delete': 'destroy'})),
    path(f'{API_VERSION_1}/message/create/', MessageCreateView.as_view({'post': 'create'})),

    # services routes
    path(f'{API_VERSION_1}/client_types/', ClientTypesView.as_view({'get': 'list'})),
    path(f'{API_VERSION_1}/industries/', IndustriesView.as_view({'get': 'list'})),
]
