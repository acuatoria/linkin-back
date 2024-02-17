from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from ..url.models import UrlUser
from .models import User


class UrlUserInline(admin.TabularInline):
    model = UrlUser
    extra = 0
    exclude = ('collection',)


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'get_url_count']
    inlines = [UrlUserInline,]

    def get_url_count(self, obj):
        return obj.urluser_set.all().count()
