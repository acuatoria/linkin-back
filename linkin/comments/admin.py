from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class UrlAdmin(admin.ModelAdmin):
    pass
