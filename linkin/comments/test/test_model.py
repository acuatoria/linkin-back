from nose.tools import eq_, ok_

from django.test import TestCase
from django.forms.models import model_to_dict

from .factories import CommentFactory
from ..models import Comment


class TestCommentModel(TestCase):

    def setUp(self):
        self.comment = CommentFactory.build()
        self.comment_data = model_to_dict(self.comment)

    def test_comment_create(self):
        self.comment_data['url'] = self.comment.url
        self.comment_data['user'] = self.comment.user

        instance = Comment(**self.comment_data)
        ok_(instance.id)
        eq_(instance.comment, self.comment_data.get('comment'))

        ok_(instance.is_owner(self.comment.user))
