from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.nested import RecipeNestedSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.constants import LENGTH_CHAR_FIELD, LENGTH_EMAIL, USERNAME_PATTERN
from users.mixins import IsSubscribedMixin
from users.validators import PatternValidator

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания пользователя."""

    email = serializers.EmailField(
        max_length=LENGTH_EMAIL,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message='Этот адрес уже занят!',
            ),
        ],
    )
    first_name = serializers.CharField(
        max_length=LENGTH_CHAR_FIELD,
    )
    last_name = serializers.CharField(
        max_length=LENGTH_CHAR_FIELD,
    )
    username = serializers.CharField(
        max_length=LENGTH_CHAR_FIELD,
        validators=[
            PatternValidator(pattern=USERNAME_PATTERN),
            UniqueValidator(
                queryset=User.objects.all(),
                message='Это имя пользователя уже занято!',
            ),
        ]
    )
    password = serializers.CharField(
        max_length=LENGTH_CHAR_FIELD,
        style={"input_type": "password"},
        write_only=True
    )

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
        read_only_fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
