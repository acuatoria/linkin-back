from django.db.models import F
from django.core.cache import cache

from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Comment
from linkin.url.models import Url
from linkin.common.permissions import IsUserOwner
from .serializers import CommentSerializer


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin
                     ):

    def perform_destroy(self, instance):
        instance.delete()
        Url.objects.filter(id=instance.url).update(comments=F('comments')-1)

    def get_object(self):
        return Comment.get(
            self.kwargs.get('pk'),
            str(self.request.user.id)
        )

    def retrieve(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        object_uuid = self.kwargs.get('pk')
        url = self.request.GET.get('url')
        if object_uuid:
            return list(Comment.query(object_uuid))
        if url:
            return [item for item in Comment.query(url, Comment.user == str(self.request.user.id))]
        return []

    queryset = []
    # Remove pagination due to incompatibility with dynamodb query
    pagination_class = None
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsUserOwner,)
