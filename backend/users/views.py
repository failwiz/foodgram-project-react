from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.viewsets import GenericViewSet, mixins

from recipes.pagination import PageLimitPagination
from users.mixins import GenericSubscriptionMixin
from users.serializers import SubscriptionSerializer


User = get_user_model()


class CustomUserViewset(UserViewSet):
    """Вьюсет для модели пользователя, наследованный от djoser."""
    pass


class UserSubViewset(
    GenericSubscriptionMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """Вьюсет для подписок на пользователей."""

    serializer_class = SubscriptionSerializer
    pagination_class = PageLimitPagination
    sub_to_model = User
    url_var = 'user_id'
    attr_name = 'subscriptions'
    already_subbed_message = 'Уже есть подписка на этого пользователя.'
    not_subbed_message = ('Невозможно отписаться от пользователя, '
                          'на которого нет подписки.')

    def get_queryset(self):
        return self.request.user.subscriptions.all().order_by('id')
