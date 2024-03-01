from django.contrib.auth import get_user_model
from djoser import utils
from djoser.conf import settings
from djoser.views import (
    update_session_auth_hash,
    UserViewSet,
)
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework.response import Response

from recipes.pagination import PageLimitPagination
from users.mixins import GenericSubscriptionMixin
from users.serializers import SubscriptionSerializer


User = get_user_model()


class CustomUserViewset(UserViewSet):
    """Вьюсет для модели пользователя, наследованный от djoser."""
    pagination_class = PageLimitPagination

    def get_permissions(self):
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.current_user
        return super().get_permissions()

    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)

    def set_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.request.user.set_password(serializer.data["new_password"])
        self.request.user.save()

        if settings.LOGOUT_ON_PASSWORD_CHANGE:
            utils.logout_user(self.request)
        elif settings.CREATE_SESSION_ON_LOGIN:
            update_session_auth_hash(self.request, self.request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
