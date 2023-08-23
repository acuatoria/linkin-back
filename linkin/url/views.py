import uuid

from django.db.models import Q
from django.db.models.aggregates import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from linkin.url.models import Url, UrlUser, Category, Collection
from linkin.common.permissions import IsUserOwner, IsUserOwnerOrPublic
from linkin.url.serializers import (
    UrlSerializer, UrlUserSerializer, CategorySerializer, CollectionSerializer,
    UrlUserMinSerializer
)


class UrlViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet,
                 ):
    """
    Lists and details Urls
    """
    queryset = Url.objects.none()
    serializer_class = UrlSerializer
    permission_classes = (AllowAny,)

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
            exclude(hide_from_public=True).\
            annotate(popular=Count('urluser')).\
            order_by('-popular', '-created_at')

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
        collection_search = self.request.query_params.get('collection')
        string = Q()
        category = Q()
        collection = Q()

        if query:
            string = (Q(description__icontains=query) | Q(url__url__icontains=query))
        if category_search:
            category = Q(category=category_search)
        if collection_search:
            collection = Q(collection=uuid.UUID(collection_search))
        return UrlUser.objects.\
            filter(user=self.request.user).\
            filter(string).\
            filter(category).\
            filter(collection).\
            select_related('url', 'user').\
            prefetch_related('collection').\
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


class CollectionViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.ListModelMixin):

    def list(self, request, *args, **kwargs):
        if self.request.user and self.request.user.is_authenticated:
            self.queryset = Collection.objects.\
                filter(user=self.request.user)
        else:
            self.queryset = Collection.objects.none()
        return super().list(request, *args, **kwargs)

    pagination_class = None
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsUserOwnerOrPublic,)


class UrlUserMinViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin):

    def get_queryset(self):
        query = self.request.query_params.get('query')
        category_search = self.request.query_params.get('category_search')
        string = Q()
        category = Q()
        if query:
            string = (Q(url__url__icontains=query) | Q(url__title__icontains=query))
        if category_search:
            category = Q(category=category_search)
        return UrlUser.objects.\
            filter(string).\
            filter(category).\
            filter(collection=self.request.query_params.get('collection')).\
            order_by('-created_at')

    queryset = UrlUser.objects.all()
    serializer_class = UrlUserMinSerializer
    permission_classes = (IsUserOwnerOrPublic,)


class UrlPublicViewSet(mixins.CreateModelMixin,
                 viewsets.GenericViewSet,
                 ):
    """
    For public create url, for the chrome addon
    """

    queryset = Url.objects.none()
    serializer_class = UrlSerializer
    permission_classes = (AllowAny,)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if request.POST.get('url'):
            url = Url.objects.filter(url=request.POST.get('url')).first()
            if url:
                serializer = self.get_serializer(url)
                return Response(serializer.data)
        return super().create(request, *args, **kwargs)
