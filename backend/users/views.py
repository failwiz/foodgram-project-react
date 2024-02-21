from django.contrib.auth import get_user_model
# from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from users.serializers import (
    UserSubsSerializer
)


User = get_user_model()


class UserSubViewset(ModelViewSet):

    serializer_class = UserSubsSerializer

    def get_queryset(self):
        return self.request.user.subscriptions
