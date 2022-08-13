from rest_framework import serializers

from .models import Comment
from linkin.url.models import Url


class CommentSerializer(serializers.ModelSerializer):

    url = serializers.PrimaryKeyRelatedField(queryset=Url.objects.all())

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'url', 'user', 'comment', 'created_at', 'updated_at', 'private')
        read_only_fields = ('id', )
