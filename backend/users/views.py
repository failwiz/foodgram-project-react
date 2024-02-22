from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet, mixins

from users.mixins import GenericSubscriptionMixin
from users.serializers import SubscriptionSerializer


User = get_user_model()


class UserSubViewset(
    GenericSubscriptionMixin,
    mixins.ListModelMixin,
    GenericViewSet
):

    serializer_class = SubscriptionSerializer
    sub_to_model = User
    url_var = 'user_id'
    attr_name = 'subscriptions'

    def get_queryset(self):
        return self.request.user.subscriptions
