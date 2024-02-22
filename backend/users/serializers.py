from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.serializers import RecipeNestedSerializer


User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели пользователя для подписок."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeNestedSerializer(many=True, read_only=True)

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
