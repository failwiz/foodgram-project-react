from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework import serializers

from recipes.nested import RecipeNestedSerializer
from users.mixins import IsSubscribedMixin


User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            settings.USER_ID_FIELD,
            'username',
            'first_name',
            'last_name',
            'password',
        )


class CustomUserSerializer(UserSerializer, IsSubscribedMixin):
    """Сериализатор модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        read_only_fields = (settings.LOGIN_FIELD,)


class SubscriptionSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    """Сериализатор модели пользователя для подписок."""

    recipes = RecipeNestedSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
