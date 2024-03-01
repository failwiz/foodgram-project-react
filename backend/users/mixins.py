from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins


class GenericSubscriptionMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):

    serializer_class = None
    sub_to_model = None
    url_var = None
    already_subbed_message = None
    not_subbed_message = None

    def get_object(self):
        obj = get_object_or_404(
            self.sub_to_model,
            pk=self.kwargs.get(self.url_var)
        )
        return obj

    @property
    def get_many_related_manager(self):
        return getattr(self.request.user, self.attr_name)

    def create(self, request, *args, **kwargs):
        if self.get_object() in self.get_many_related_manager.all():
            return Response(
                data=self.already_subbed_message,
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = self.get_serializer(self.get_object())
        headers = self.get_success_headers(serializer.data)
        self.get_many_related_manager.add(self.get_object())
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        if self.get_object() not in self.get_many_related_manager.all():
            return Response(
                data=self.not_subbed_message,
                status=status.HTTP_400_BAD_REQUEST
            )
        self.get_many_related_manager.remove(self.get_object())
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class IsSubscribedMixin:
    """Миксин для поля подписки в сериализаторе."""

    def get_is_subscribed(self, obj):
        return (
            False if self.context.get('request').user.is_anonymous
            else obj in self.context.get('request').user.subscriptions.all()
        )
