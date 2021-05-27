from django.db.models import Count
from django.db.models.functions import TruncDay
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import views
from rest_framework import generics
from rest_framework.response import Response

from .models import Post, Like
from .serializers import PostSerializer, LikeAnalyticsSerializer


class IsPostOwnerPermission(permissions.BasePermission):
    """
    Allow :model:`blog.Post` owners to edit their posts.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be edited by their owners and viewed by all authenticated users.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerPermission]


class LikeView(views.APIView):
    """
    API endpoint that allows adding or removing likes to posts.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id, format=None):
        try:
            Like.objects.get(user=request.user, post=Post.objects.get(id=post_id))
            return Response('Liked')
        except Like.DoesNotExist:
            return Response('Not liked')

    def put(self, request, post_id, format=None):
        Like.objects.get_or_create(user=request.user, post=Post.objects.get(id=post_id))
        return Response("OK")

    def delete(self, request, post_id, format=None):
        try:
            Like.objects.get(user=request.user, post=Post.objects.get(id=post_id)).delete()
        except Like.DoesNotExist:
            pass
        return Response("OK")


class LikeDateFilter(filters.FilterSet):
    """
    Filter by dates in the range.
    """
    date_from = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    date_to = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Like
        fields = ['created_at', ]


class LikeAnalyticsView(generics.ListAPIView):
    """
    API endpoint that returns analytics about how many likes were made by user aggregated by day.
    """
    permission_classes = [permissions.IsAuthenticated]

    queryset = Like.objects.all()
    serializer_class = LikeAnalyticsSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = LikeDateFilter

    def get_queryset(self):
        queryset = self.queryset.filter(user_id=self.kwargs.get('user_id'))
        queryset = queryset.annotate(day=TruncDay('created_at')).values('day').annotate(count=Count('id')).order_by(
            "-day")
        return queryset
