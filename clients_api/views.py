from rest_framework import generics
from rest_framework.response import Response

from clients.models import Clients, Industries
from .serializers import ClientsSerializer


class ClientsList(generics.ListCreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer


class ClientDetail(generics.RetrieveDestroyAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
