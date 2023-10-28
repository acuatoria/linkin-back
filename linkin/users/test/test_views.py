import factory
from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker

from django.urls import reverse
from django.contrib.auth.hashers import check_password
from django.forms.models import model_to_dict

from ..models import User
from .factories import UserFactory

fake = Faker()


class TestUserListTestCase(APITestCase):
    """
    Tests /users list operations.
    """
    def setUp(self):
        self.url = reverse('user-list')
        self.user_data = factory.build(dict, FACTORY_CLASS=UserFactory)
        self.user_data['recaptcha'] = 'test_token'

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(pk=response.data.get('id'))
        self.assertEquals(user.username, self.user_data.get('username'))
        self.assertTrue(check_password(self.user_data.get('password'), user.password))


class TestUserDetailTestCase(APITestCase):
    """
    Tests /users detail operations.
    """

    def setUp(self):
        self.user = UserFactory()
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def test_get_request_returns_a_given_user(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_put_request_updates_a_user(self):
        new_first_name = fake.first_name()
        payload = {'first_name': new_first_name}
        response = self.client.put(self.url, payload)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

        user = User.objects.get(pk=self.user.id)
        self.assertEquals(user.first_name, new_first_name)


class TestUserLogin(APITestCase):
    """
    Test user login
    """

    def setUp(self) -> None:
        self.user = UserFactory()
        self.url = reverse('rest_framework:login')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')

    def test_login(self):
        response = self.client.post(self.url, {'username':self.user.username, 'password': self.user.password})
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        self.url = reverse('rest_framework:logout')
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)