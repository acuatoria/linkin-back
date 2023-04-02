from faker import Faker

from django.test import TestCase

from linkin.users.models import User

fake = Faker()


class UserModelTest(TestCase):
    
    def test_user_create(self):
        user = User.objects.create(email=fake.email(), username='test')
        self.assertEqual(user.__str__(), 'test')