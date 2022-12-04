from django.urls import path
from .views import ClientsListView, ClientDetailView, MessagesListView, MessagesCreateView


app_name = 'clients_api'

urlpatterns = [
    path('', ClientsListView.as_view()),
    path('<int:pk>/', ClientDetailView.as_view()),
    path('messages/', MessagesListView.as_view())
]
