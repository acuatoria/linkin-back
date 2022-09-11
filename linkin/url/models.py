import uuid
from gettext import gettext as _

from django.db import models
from django.contrib.postgres.fields import ArrayField

from linkin.common.model_permissions import ModelPermissions


MAX_URL_SIZE = 2048


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Url(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # This field should be calculated based on categories of url user
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    show_on_front = models.BooleanField(default=False)

    # this field will be filled automatically
    title = models.TextField(null=True, blank=True)

    url = models.URLField(unique=True, max_length=MAX_URL_SIZE)

    def __str__(self):
        return f'{self.url}'


class UrlUser(ModelPermissions):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    url = models.ForeignKey(Url, on_delete=models.CASCADE)

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)

    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('User description about this url (private)')
    )

    tags = ArrayField(
        base_field=models.CharField(max_length=100, null=True, blank=True),
        verbose_name=_('User tags'),
        null=True, blank=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.url} - {self.user}'

    def is_owner(self, user):
        return self.user == user
