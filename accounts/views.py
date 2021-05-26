from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

from .serializers import UserSerializer


class CreateUserPermission(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return True

        return super(CreateUserPermission, self).has_permission(request, view)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [CreateUserPermission]
