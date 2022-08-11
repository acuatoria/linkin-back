from rest_framework import serializers

from .models import Url, UrlUser


class UrlSerializer(serializers.ModelSerializer):

    class Meta:
        model = Url
        fields = ('id', 'url', 'category')
        read_only_fields = ('id', 'category')


class UrlUserSerializer(serializers.ModelSerializer):

    url = serializers.StringRelatedField(read_only=True)

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    url_string = serializers.CharField(write_only=True)

    username = serializers.SerializerMethodField()

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UrlUser
        fields = ('id', 'description', 'user', 'url', 'url_string', 'username', 'category')

    def create(self, validated_data):
        url_string = validated_data.pop('url_string')
        url_object, _ = Url.objects.get_or_create(url=url_string)
        url_user, _ = UrlUser.objects.update_or_create(
            user=validated_data.get('user'),
            url=url_object,
            defaults={**validated_data})
        return url_user
