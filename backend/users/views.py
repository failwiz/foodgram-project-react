from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users.models import Subscription
from users.serializers import SubscriptionSerializer


User = get_user_model()


class SubscriptionViewSet(ModelViewSet):
    """Вьюсет для модели подписок."""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated, )
    filter_backends = (SearchFilter,)
    search_fields = ('subscribed_to__username',)

    @property
    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def get_queryset(self):
        return self.request.user.subscribed_to.all()

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            subscription=self.get_user,
        )

    def get_object(self):
        return get_object_or_404(
            Subscription,
            user=self.request.user,
            subscription=self.get_user,
        )

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_404_NOT_FOUND)
