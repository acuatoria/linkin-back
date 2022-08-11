from django.contrib import admin

from .models import Url, UrlUser


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    pass

@admin.register(UrlUser)
class UrlUserAdmin(admin.ModelAdmin):
    pass
