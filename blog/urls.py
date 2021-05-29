from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'posts', views.PostViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('posts/<int:post_id>/like/', views.LikeView.as_view(), name='post-like'),
    path('users/<int:user_id>/analytics/', views.LikeAnalyticsView.as_view(), name='user-analytics')
]
