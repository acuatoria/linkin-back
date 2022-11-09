from datetime import datetime

from django.db.models import F

from rest_framework import serializers

from linkin.comments.models import Comment
from linkin.url.models import Url


class CommentSerializer(serializers.Serializer):

    url = serializers.CharField(max_length=200)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    comment = serializers.CharField(max_length=1024)
    user_name = serializers.ReadOnlyField()
    updated_at = serializers.ReadOnlyField()

    def validate_url(self, value):
        if not Url.objects.filter(id=value).exists():
            raise serializers.ValidationError("Url doesn't exists")
        return value

    def create(self, validated_data):
        url = validated_data.get('url')
        user = str(validated_data.get('user').id)
        action = self.context.get('request').data.get('action')

        if action == 'add':
            comment = Comment(
                url,
                user=user,
                comment=validated_data.get('comment'),
                updated_at=datetime.now(),
                user_name=str(validated_data.get('user').username)
            )
            comment.save(Comment.url.does_not_exist() & Comment.user.does_not_exist())
            Url.objects.filter(id=comment.url).update(comments=F('comments')+1)
            return comment

        if action == 'update':
            comment = Comment.get(url, user)
            comment.update(
                actions=[
                    Comment.comment.set(validated_data.get('comment')),
                    Comment.updated_at.set(datetime.now())
                ]
            )
            return comment
