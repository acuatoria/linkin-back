from django.test import TestCase

from .factories import CommentFactory
from ..models import Comment


class TestCommentModel(TestCase):
    comment_data = CommentFactory()

    def test_comment_create(self):
        comment = Comment(**self.comment_data)
        comment.save()
        self.assertTrue(comment)
        
    def test_comment_delete(self):
        comment = Comment.get(
            self.comment_data.get('url'),
            self.comment_data.get('user')
        )
        self.assertTrue(comment.delete())