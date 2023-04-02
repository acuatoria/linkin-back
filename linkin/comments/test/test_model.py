from nose.tools import eq_, ok_

from django.test import TestCase

from .factories import CommentFactory
from ..models import Comment


class TestCommentModel(TestCase):
    comment_data = CommentFactory()

    def test_comment_create(self):
        comment = Comment(**self.comment_data)
        comment.save()
        ok_(comment)
        
    def test_comment_delete(self):
        comment = Comment.get(
            self.comment_data.get('url'),
            self.comment_data.get('user')
        )
        ok_(comment.delete())