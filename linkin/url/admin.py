from django.contrib import admin

from .models import Category, Url, UrlUser


@admin.register(Url)
class UrlAdmin(admin.ModelAdmin):
    ordering = ('-created_at', )
    list_display = ('created_at', 'url')


@admin.register(UrlUser)
class UrlUserAdmin(admin.ModelAdmin):
    ordering = ('-created_at', )
    list_display = ('created_at', 'url')
    exclude = ('collection',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
