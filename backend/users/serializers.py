from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.serializers import RecipeSerializer


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(many=True, read_only=True)

    def get_is_subscribed(self, obj):
        return obj in self.context.get('request').user.subscriptions.all()

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
        )
