from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'get_url_count']

    def get_url_count(self, obj):
        return obj.urluser_set.all().count()
