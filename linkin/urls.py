
from django.contrib import admin
from django.conf import settings
from django.http import HttpResponse
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from django.urls import path, re_path, include, reverse_lazy

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from reset_password.views import ResetPasswordView

from .comments.views import CommentViewSet
from linkin.url.views import (
    UrlViewSet, UrlUserCreateViewSet, CategoryViewSet, CollectionViewSet,
    UrlUserMinViewSet, UrlPublicViewSet
)
from .users.views import UserViewSet, UserCreateViewSet


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'users', UserCreateViewSet)
router.register(r'comments', CommentViewSet, basename="comments")
router.register(r'urls', UrlViewSet)
router.register(r'urlpub', UrlPublicViewSet, basename="urlpub")
router.register(r'url-user', UrlUserCreateViewSet, basename="url-user")
router.register(r'category', CategoryViewSet)
router.register(r'collection', CollectionViewSet)
router.register(r'urluser-min', UrlUserMinViewSet)
router.register(r'reset-password', ResetPasswordView, basename="reset_password")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('loaderio-c16a286f8471124641c4f0cfb17b67a7.txt', lambda _: HttpResponse(open('loaderio-c16a286f8471124641c4f0cfb17b67a7.txt', 'r'), content_type='text/plain')),

    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
