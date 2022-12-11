from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from django_currentuser.middleware import get_current_authenticated_user

from clients.models import Clients, Messages, Industries
from .serializers import ClientsSerializer, MessagesSerializer, ClientsListSerializer


class ClientsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get for read only list of clients and retrieve single object of client
    """
    queryset = Clients.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        elif self.request.user.is_admin:
            return queryset.filter(user__company=self.request.user.company)
        elif self.request.user.is_employee and not self.request.user.is_admin:
            return queryset.filter(user=self.request.user)
        elif not self.request.user.is_employee or not self.request.user.is_admin or not self.request.user.is_superuser:
            raise PermissionDenied(detail="You do not have permission for this action!")
        return queryset

    # def get_object(self):
    #     obj = super().get_object()
    #     if (
    #             self.request.user.is_superuser or
    #             (self.request.user.is_admin and self.request.user.company == obj.user.company) or
    #             (self.request.user.is_employee and self.request.user.id == obj.user.id)
    #     ):
    #         return obj
    #     else:
    #         raise PermissionDenied(detail="You do not have permission for this action!")

    def get_serializer_class(self):
        if self.action == 'list':
            return ClientsListSerializer
        elif self.action == 'retrieve':
            return ClientsSerializer


class MessagesViewSet(mixins.CreateModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    queryset = Messages.objects.all()
    serializer_class = MessagesSerializer

    # def get_queryset(self, *args, **kwargs):
    #     data = self.request.data
    #     return super().get_queryset()


class MessagesCreateView(APIView):
    def post(self, request):
        message = MessagesSerializer(data=request.data)
        if message.is_valid():
            message.save()
        return Response(status=201)
