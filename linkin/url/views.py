from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from linkin.url.models import Url, UrlUser, Category
from linkin.common.permissions import IsUserOwner
from linkin.url.serializers import UrlSerializer, UrlUserSerializer, CategorySerializer


class UrlViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet,
                 ):
    """
    Lists and details Urls
    """
    queryset = Url.objects.none()
    serializer_class = UrlSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_object(self):
        return get_object_or_404(Url, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        query = self.request.query_params.get('query')
        category_search = self.request.query_params.get('category_search')
        string = Q()
        category = Q()
        if query:
            string = (Q(url__icontains=query) | Q(title__icontains=query))
        if category_search:
            category = Q(category=category_search)
        return Url.objects.\
            filter(string).\
            filter(category).\
            filter(public=True).\
            order_by('-updated_at')

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
        query = self.request.query_params.get('query')
        category_search = self.request.query_params.get('category_search')
        string = Q()
        category = Q()
        if query:
            string = (Q(description__icontains=query) | Q(url__url__icontains=query))
        if category_search:
            category = Q(category=category_search)
        return UrlUser.objects.\
            filter(user=self.request.user).\
            filter(string).\
            filter(category).\
            order_by('-created_at')

    queryset = UrlUser.objects.none()
    serializer_class = UrlUserSerializer
    permission_classes = (IsAuthenticated, IsUserOwner,)


class CategoryViewSet(mixins.RetrieveModelMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet,
                      ):
    """
    Lists and details Urls
    """
    pagination_class = None
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @method_decorator(cache_page(60*60))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
