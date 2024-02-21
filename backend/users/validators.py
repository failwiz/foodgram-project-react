from django.core.exceptions import ValidationError


class UserNotSubbedToSelfValidator:
    """Валидатор проверки, что пользователь не может подписаться на себя."""

    def __init__(
            self, user_field='user',
            subscription_field='subscription',
            message='Пользователь не может подписаться на себя.'
    ):
        self.user_field = user_field
        self.subscription_field = subscription_field
        self.message = message

    def __call__(self, attrs):
        if attrs[self.user_field] == attrs[self.subscription_field]:
            raise ValidationError(self.message)
