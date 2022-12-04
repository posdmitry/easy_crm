from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Clients, Messages, Industries
from .serializers import ClientsSerializer, MessagesSerializer


class ClientsListView(generics.ListCreateAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClientDetailView(generics.RetrieveDestroyAPIView):
    queryset = Clients.objects.all()
    serializer_class = ClientsSerializer


class MessagesListView(generics.ListCreateAPIView):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    def get_queryset(self, *args, **kwargs):
        data = self.request.data
        return super().get_queryset()


class MessagesCreateView(APIView):
    def post(self, request):
        message = MessagesSerializer(data=request.data)
        if message.is_valid():
            message.save()
        return Response(status=201)
