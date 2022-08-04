from django.test import TestCase
from django.forms.models import model_to_dict
from nose.tools import eq_, ok_
from .factories import CommentFactory
from ..serializers import CommentSerializer


class TestCreateCommentSerializer(TestCase):

    def setUp(self):
        self.comment = CommentFactory.build()
        self.comment_data = model_to_dict(self.comment)

    def test_serializer_with_empty_data(self):
        request = self.client.request()
        request.user = self.comment.user
        serializer = CommentSerializer(data={}, context={
            'request': request})
        eq_(serializer.is_valid(), False)

    def test_serializer_with_valid_data(self):
        request = self.client.request()
        request.user = self.comment.user
        serializer = CommentSerializer(data=self.comment_data, context={
            'request': request}
        )
        self.comment.url.save()
        ok_(serializer.is_valid())

        url = self.comment.url
        user = self.comment.user
        eq_(str(self.comment), f'{url} - {user}')
