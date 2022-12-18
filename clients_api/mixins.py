from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied

from clients_api.serializers import ClientsListSerializer


class CustomClientsQuerySetMixin:
    """
    Handle querysets for 'list' and 'retrieve' endpoints for Clients
    """
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        elif self.request.user.is_admin:
            return queryset.filter(user__company=self.request.user.company)
        elif self.request.user.is_employee and not self.request.user.is_admin:
            return queryset.filter(user=self.request.user)
        elif not (self.request.user.is_employee and self.request.user.is_admin) and not self.request.user.is_superuser:
            raise PermissionDenied(detail="You do not have permission for this action!")
        return queryset


class GetSerializerMixin:
    """
    Get serializer class in order to endpoint action
    """
    serializer_class = None
    serializer_requests_classes = {}

    def get_serializer_class(self):
        return self.serializer_requests_classes.get(self.action, self.serializer_class)

