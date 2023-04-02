from django.test import TestCase

from faker import Faker

from .factories import UrlUserFactory, UrlFactory
from linkin.users.test.factories import UserFactory
from linkin.url.models import UrlUser

fake = Faker()


class UrlUserTest(TestCase):
    
    def setUp(self):
        self.url = fake.url()

    def testCreateUrlUser(self):
        url = UrlFactory.create(url=self.url)
        user = UserFactory()
        urluser = UrlUser.objects.create(url=url, user=user, public=False)
        self.assertEqual(urluser.url.__str__(), self.url)