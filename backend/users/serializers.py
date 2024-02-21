from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.validators import UserNotSubbedToSelfValidator
from users.models import Subscription


User = get_user_model()


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор модели подписки."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    subscription = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
    )

    class Meta:
        model = Subscription
        fields = ('user', 'subscription')

        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=('user', 'subscription')
            ),
            UserNotSubbedToSelfValidator(
                user_field='user',
                subscription_field='subscription'
            )
        ]
