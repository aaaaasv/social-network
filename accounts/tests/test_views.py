from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer

User = get_user_model()

factory = APIRequestFactory()


class AuthViewsTestCase(TestCase):
    fixtures = ['user-data.json']

    def setUp(self):
        self.client = APIClient()
        self.login_data = {
            'username': 'admin',
            'password': 'development'
        }

    def obtain_token_pair(self, user_data):
        response = self.client.post(reverse('token_obtain_pair'), user_data, format='json')
        return response

    def verify_access_token(self, token):
        token = {
            'token': token
        }
        response = self.client.post(reverse('token_verify'), token)
        return response

    def test_user_signup_fail(self):
        response = self.client.post(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_signup_success(self):
        signup_data = {
            'username': 'test_username',
            'password': 'test_password123'
        }
        response = self.client.post(reverse('user-list'), signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], signup_data['username'])
        self.assertTrue(User.objects.filter(username='test_username').exists())

    def test_user_access_token_obtain_fail(self):
        login_data_wrong = {
            'username': 'admin',
            'password': 'wrong_password123'
        }
        response = self.obtain_token_pair(login_data_wrong)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)

    def test_user_access_token_obtain_success(self):
        response = self.obtain_token_pair(self.login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        response_verification = self.verify_access_token(response.data['access'])
        self.assertEqual(response_verification.status_code, status.HTTP_200_OK)


class SetUpTestCase(TestCase):
    fixtures = ['user-data.json']

    def obtain_token_pair(self, user_data):
        response = self.client.post(reverse('token_obtain_pair'), user_data, format='json')
        return response

    def setUp(self):
        self.client = APIClient()
        self.client_authorized_admin = APIClient()
        self.client_authorized = APIClient()
        self.login_data_admin = {
            'username': 'admin',
            'password': 'development'
        }

        self.login_data = {
            'username': 'myname3',
            'password': 'development'
        }
        self.user_id = User.objects.get(username=self.login_data['username']).id
        self.client_authorized_admin.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.obtain_token_pair(self.login_data_admin).data['access'])

        self.client_authorized.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.obtain_token_pair(self.login_data).data['access'])


class UsersTestCase(SetUpTestCase):

    def test_get_all_users_fail_unauthorized(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_users_success_authorized(self):
        response = self.client_authorized.get(reverse('user-list'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': factory.get(reverse('user-list'))})
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_one_user_fail_unauthorized(self):
        response = self.client.get(reverse('user-detail', kwargs={'pk': User.objects.all().first().id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_one_user_success_authorized(self):
        user = User.objects.first()
        response = self.client_authorized.get(reverse('user-detail', kwargs={'pk': user.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('username', response.data)
        self.assertEqual(response.data['id'], user.id)

    def test_update_user_fail_forbidden_not_owner(self):
        user = User.objects.first()
        user_id = user.id
        self.assertNotEqual(self.user_id, user_id)
        response = self.client_authorized.put(reverse('user-detail', kwargs={'pk': user_id}),
                                              {'first_name': 'Newname'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_success_owner(self):
        user_id = self.user_id
        new_first_name = 'Newname'
        self.assertNotEqual(User.objects.get(id=user_id).first_name, new_first_name)
        response = self.client_authorized.put(reverse('user-detail', kwargs={'pk': user_id}),
                                              {'first_name': new_first_name})

        self.assertNotIn('password', response.data)
        self.assertNotIn('username', response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.get(id=user_id).first_name, new_first_name)

    def test_delete_user_success_owner(self):
        user_id = self.user_id
        response = self.client_authorized.delete(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)

    def test_delete_user_fail_unauthorized(self):
        user = User.objects.first()
        user_id = user.id
        response = self.client.delete(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_fail_forbidden_not_owner(self):
        user = User.objects.first()
        user_id = user.id
        response = self.client_authorized.delete(reverse('user-detail', kwargs={'pk': user_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
