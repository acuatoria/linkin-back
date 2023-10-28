from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker

from linkin.url.test.factories import UrlFactory
from linkin.users.test.factories import UserFactory

fake = Faker()

'''
· An user comment only is modified by its user 

· A user can create user comment

· Private comments are filtered

'''
class TestCommentViewSetDetail(APITestCase):
    """
    Tests /users list operations.
    """
    def setUp(self):

        self.user = UserFactory()
        self.url = reverse('user-detail', kwargs={'pk': self.user.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.user.auth_token}')
        
        url = UrlFactory.build()
        url.save()

        self.comment = {'url':url.id, 'user':self.user.id, 'user_name':self.user.username, 'comment':fake.city(), 'action': 'add'}
        self.url = reverse('comments-list')

    def test_post_request_with_no_data_fails(self):
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_request_with_valid_data_succeeds(self):
        response = self.client.post(self.url, self.comment)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
