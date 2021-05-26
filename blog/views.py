from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer


class IsPostOwnerPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows posts to be edited by their owners and viewed.
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsPostOwnerPermission]


class LikeView(views.APIView):
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
