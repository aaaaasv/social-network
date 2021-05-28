from django.contrib.auth import get_user_model
from rest_framework import (
    viewsets,
    permissions,
    generics
)

from .serializers import (
    UserSerializer,
    UserActivitySerializer,
)

User = get_user_model()


class CreateUserPermission(permissions.IsAdminUser):
    """
    Allow everyone to create users and only admins to view the list of users.
    """

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


class UserActivityView(generics.RetrieveAPIView):
    """
    API endpoint that allows user's information about last login and last request made to be viewed.
    """
    model = User
    queryset = User.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        queryset = User.objects.filter(pk=self.kwargs.get('pk')).values('last_login', 'last_request')
        return queryset
