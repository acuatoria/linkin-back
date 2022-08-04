import uuid
from gettext import gettext as _

from django.db import models
from django.contrib.postgres.fields import ArrayField

from linkin.common.model_permissions import ModelPermissions


CATEGORIES = (
    ('Social networks and online communities', 'Social networks and online communities'),
    ('News and media', 'News and media'),
    ('Search engines', 'Search engines'),
    ('Marketplace', 'Marketplace'),
    ('Adult', 'Adult'),
    ('Programming and developer software', 'Programming and developer software'),
    ('TV movies and streaming', 'TV movies and streaming'),
    ('Email', 'Email'),
    ('Blog', 'Blog'),
    ('Forum or wiki', 'Forum or wiki'),
    ('Business website', 'Business website'),
    ('Portfolio', 'Portfolio'),
    ('Crowdfunding', 'Crowdfunding'),
    ('Magazine', 'Magazine'),
    ('Educational', 'Educational'),
)


class Url(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # This field must be calculated based on categories of url user
    category = models.CharField(
        blank=True, null=True,
        max_length=200,
        verbose_name=_('Url category'),
        choices=CATEGORIES
    )

    show_on_front = models.BooleanField(default=False)

    url = models.URLField(unique=True)

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

    category = models.CharField(
        blank=True, null=True,
        max_length=200,
        verbose_name=_('Url category'),
        choices=CATEGORIES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.url} - {self.user}'

    def is_owner(self, user):
        return self.user == user
