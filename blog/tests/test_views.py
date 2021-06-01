from datetime import datetime
import pytz

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status

from accounts.tests.test_views import SetUpTestCase
from blog.models import Post, Like
from blog.views import LikeAnalyticsView
from blog.serializers import PostSerializer

User = get_user_model()

factory = APIRequestFactory()


class PostTestCase(SetUpTestCase):
    fixtures = SetUpTestCase.fixtures + ['post-data.json']

    def setUp(self):
        super(PostTestCase, self).setUp()
        self.post_text = 'New post text'

    @staticmethod
    def is_post_liked(post_id, user_id):
        return Like.objects.filter(post_id=post_id, user_id=user_id).exists()

    def test_get_post_list_fail_unauthorized(self):
        response = self.client.get(reverse('post-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_post_list_success(self):
        response = self.client_authorized.get(reverse('post-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        posts = Post.objects.all()
        serializer = PostSerializer(reversed(posts), many=True, context={'request': factory.get(reverse('post-list'))})

        self.assertSequenceEqual(response.data.get('results'), serializer.data)

    def test_create_post_fail_unauthorized(self):
        response = self.client.post(reverse('post-list'), {'text': self.post_text})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_success(self):
        response = self.client_authorized.post(reverse('post-list'), {'text': self.post_text})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(self.post_text, Post.objects.get(id=response.data['id']).text)

    def test_post_add_like_fail_unauthorized(self):
        response = self.client.post(reverse('post-like', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_add_like_success(self):
        response = self.client_authorized.post(reverse('post-like', kwargs={'post_id': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.is_post_liked(user_id=self.user_id, post_id=2))
        self.assertEqual(response.data, 'OK')

    def test_post_delete_like_fail_unauthorized(self):
        response = self.client.delete(reverse('post-like', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_delete_like_success(self):
        self.assertTrue(self.is_post_liked(user_id=self.user_id, post_id=1))
        response = self.client_authorized.delete(reverse('post-like', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.is_post_liked(user_id=self.user_id, post_id=1))
        self.assertEqual(response.data, 'OK')

    def test_post_get_like_info_liked(self):
        response = self.client_authorized.get(reverse('post-like', kwargs={'post_id': 1}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.is_post_liked(user_id=self.user_id, post_id=1))
        self.assertEqual(response.data, 'Liked')

    def test_post_get_like_info_not_liked(self):
        response = self.client_authorized.get(reverse('post-like', kwargs={'post_id': 2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.is_post_liked(user_id=self.user_id, post_id=2))
        self.assertEqual(response.data, 'Not liked')


class LikeAnalyticsTestCase(SetUpTestCase):
    fixtures = SetUpTestCase.fixtures + ['post-data.json']

    def test_like_count_by_days(self):
        v = LikeAnalyticsView(kwargs={'user_id': 2})
        result = v.get_queryset()
        self.assertEqual(result.get(day=datetime(2020, 12, 25, 0, 0, tzinfo=pytz.UTC))['count'], 2)
        self.assertEqual(result.get(day=datetime(2019, 3, 12, 0, 0, tzinfo=pytz.UTC))['count'], 1)
