from django.contrib.auth import get_user_model
from rest_framework import (
    viewsets,
    permissions,
    generics,
)

from .serializers import (
    UserSerializer,
    UserActivitySerializer,
)

User = get_user_model()


class IsOwnerOrAdminPermission(permissions.IsAuthenticated):
    """
    Allows authenticated users to view and edit their information.
    Allow admins to view and edit every user information.
    """

    def has_permission(self, request, view):
        if request.method in ['POST']:
            return True

        return super(IsOwnerOrAdminPermission, self).has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if (request.user and request.user.is_staff) or \
                (request.user and request.user.is_authenticated and request.user == obj):
            return True
        return request.method in permissions.SAFE_METHODS


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdminPermission]


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
