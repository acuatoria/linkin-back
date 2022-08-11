from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated

from linkin.url.models import Url, UrlUser
from linkin.common.permissions import IsUserOwner
from linkin.url.serializers import UrlSerializer, UrlUserSerializer


class UrlViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet,
                 ):
    """
    Lists and details Urls
    """
    queryset = Url.objects.all()
    serializer_class = UrlSerializer
    permission_classes = (AllowAny,)

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class UrlUserCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet,
                           mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.ListModelMixin):
    """
    CRUD user's urls
    """
    def get_queryset(self):
        return UrlUser.objects.filter(user=self.request.user)

    queryset = UrlUser.objects.none()
    serializer_class = UrlUserSerializer
    permission_classes = (IsAuthenticated, IsUserOwner,)
