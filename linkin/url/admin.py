from django.contrib import admin

from .models import Category, Url, UrlUser


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    ordering = ('-id', )


@admin.register(UrlUser)
class UrlUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
