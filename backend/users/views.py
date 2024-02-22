from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from recipes.models import Recipe
from users.serializers import (
    FavoriteSerializer,
    SubscriptionSerializer
)


User = get_user_model()


class UserSubViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):

    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return self.request.user.subscriptions

    def get_user(self):
        return get_object_or_404(User, pk=self.kwargs.get('user_id'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_user())
        headers = self.get_success_headers(serializer.data)
        self.request.user.subscriptions.add(self.get_user())
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        self.request.user.subscriptions.remove(self.get_user())
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )


class UserFavViewset(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):

    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return self.request.user.favorite_recipes

    def get_recipe(self):
        return get_object_or_404(Recipe, pk=self.kwargs.get('recipe_id'))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_recipe())
        headers = self.get_success_headers(serializer.data)
        self.request.user.favorite_recipes.add(self.get_recipe())
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        self.request.user.favorite_recipes.remove(self.get_recipe())
        return Response(
            status=status.HTTP_204_NO_CONTENT,
        )
