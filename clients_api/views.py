from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from clients.models import Clients, ClientType, Industries
from .mixins import CustomClientsQuerySetMixin, GetSerializerMixin
from .serializers import (
    ClientsSerializer,
    ClientsListSerializer,
    CreateMessageSerializer,
    ClientCreateSerializer,
    ClientUpdateSerializer, ClientTypesListSerializer, IndustriesSerializer
)


class ClientsViewSet(CustomClientsQuerySetMixin, GetSerializerMixin, ModelViewSet):
    """
    Get list of clients and retrieve single object of client for read only
    """
    queryset = Clients.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClientsListSerializer
    serializer_requests_classes = {
        'list': ClientsListSerializer,
        'retrieve': ClientsSerializer,
        'create': ClientCreateSerializer,
        'update': ClientUpdateSerializer,
        'destroy': ClientsSerializer
    }

    def destroy(self, request, *args, **kwargs):
        super().destroy(self, request, *args, **kwargs)
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data=f"Client with id={kwargs.get('pk')} has successfully deleted!")


class MessageCreateView(ModelViewSet):
    """
    Create message for client view
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CreateMessageSerializer


class ClientTypesView(ReadOnlyModelViewSet):
    """
    Get list of client types
    """
    queryset = ClientType.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClientTypesListSerializer


class IndustriesView(ReadOnlyModelViewSet):
    """
    Get list of industries
    """
    queryset = Industries.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IndustriesSerializer

