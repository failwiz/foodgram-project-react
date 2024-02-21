from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    class Meta:
        model = User
        fields = '__all__'


class UserSubsSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""
    subscriptions = UserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('subscriptions', )
