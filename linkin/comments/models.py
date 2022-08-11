import uuid

from django.db import models

from linkin.common.model_permissions import ModelPermissions


class Comment(ModelPermissions):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    url = models.ForeignKey('url.Url', on_delete=models.CASCADE)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    private = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.url} - {self.user}'

    def is_owner(self, user):
        return self.user == user
