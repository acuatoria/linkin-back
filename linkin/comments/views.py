import uuid
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from .models import Comment
from linkin.common.permissions import IsUserOwner
from .serializers import CommentSerializer


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin
                     ):
    """
    Creates comments
    """
    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    queryset = Comment.objects.none()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsUserOwner,)


class CommentUrlViewSet(viewsets.GenericViewSet,
                        mixins.ListModelMixin,
                        mixins.RetrieveModelMixin
                        ):
    """
    Get comments by url
    """
    def retrieve(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        object_uuid = self.kwargs.get('pk')

        if not object_uuid:
            return Comment.objects.none()

        try:
            uuid.UUID(object_uuid)
        except ValueError:
            raise Http404("Invalid uuid")

        return Comment.objects.filter(url=object_uuid)

    queryset = Comment.objects.none()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
