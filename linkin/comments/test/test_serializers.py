from faker import Faker

from django.test import TestCase

from nose.tools import eq_, ok_
from ..serializers import CommentSerializer
from linkin.url.test.factories import UrlFactory
from linkin.users.test.factories import UserFactory

from linkin.comments.models import Comment

fake = Faker()

class TestCommentSerializer(TestCase):

    def setUp(self):
        url = UrlFactory.build()
        url.save()
        user = UserFactory.build()
        self.comment = Comment(url=url.id, user=user.id, user_name=user.username, comment=fake.city())
        self.comment_data = self.comment.attribute_values

    def test_serializer_with_empty_data(self):
        request = self.client.request()
        request.user = self.comment.user
        request.action = 'add'
        serializer = CommentSerializer(data={}, context={
            'request': request})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        request = self.client.request()
        request.user = self.comment.user
        request.action = 'update'
        serializer = CommentSerializer(data=self.comment_data, context={
            'request': request}
        )
        ok_(serializer.is_valid())
        eq_(self.comment.comment, serializer.data.get('comment'))

    def test_serializer_data(self):
        request = self.client.request()
        request.user = self.comment.user
        url = self.comment.url
        eq_(self.comment.url, url)
