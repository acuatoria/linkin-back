from rest_framework import serializers

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from .models import Url, UrlUser, Category, MAX_URL_SIZE


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

    def validate_url_string(self, value):
        """
        Check for valid url
        """
        if len(value) > MAX_URL_SIZE:
            raise serializers.ValidationError("Url too long")
        try:
            validator = URLValidator()
            validator(value)
        except ValidationError:
            raise serializers.ValidationError("Url is not valid")

        return value

    def validate_category(self, value):
        """
        Check for valid category
        """
        if not value:
            return None

        if Category.objects.filter(id=value.id).exists():
            return value

        raise serializers.ValidationError("Category is not valid")

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

    def update(self, instance, validated_data):
        url_string = validated_data.pop('url_string')
        url_object, _ = Url.objects.get_or_create(url=url_string)
        instance.url = url_object
        instance.description = validated_data.pop('description')
        instance.category_id = validated_data.pop('category')
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id', 'name')