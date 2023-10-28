from django.test import TestCase
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password

from .factories import UserFactory
from ..serializers import CreateUserSerializer


class TestCreateUserSerializer(TestCase):

    def setUp(self):
        self.user = UserFactory.build()
        self.user_data = model_to_dict(self.user)
        self.user_data['recaptcha'] = 'test_token'

    def test_serializer_with_empty_data(self):
        serializer = CreateUserSerializer(data={})
        self.assertEquals(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        self.assertEquals(str(self.user), serializer.data.get('username'))

    def test_serializer_hashes_password(self):
        serializer = CreateUserSerializer(data=self.user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(check_password(self.user_data.get('password'), user.password))
