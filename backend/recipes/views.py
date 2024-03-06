import tempfile

from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.nested import RecipeNestedSerializer
from recipes.pagination import PageLimitPagination
from recipes.permissions import IsOwnerOrReadOnly
from recipes.serializers import (IngredientSerializer,
                                 RecipeCreateUpdateSerializer,
                                 RecipeSerializer, TagSerializer)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet, mixins
from users.mixins import GenericSubscriptionMixin


class IngredientViewSet(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вьюсет для модели ингредиента."""

    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (DjangoFilterBackend,)
    pagination_class = None
    filterset_class = IngredientFilter
    filterset_fields = ['name']


class RecipeViewSet(ModelViewSet):
    """Вьюсет для модели рецепта."""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all().order_by('-pub_date')
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = PageLimitPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = [
        'tags', 'author', 'is_favorited', 'is_in_shopping_cart',
    ]

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            self.serializer_class = RecipeCreateUpdateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = RecipeSerializer(instance=instance)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=False
        )
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        serializer = RecipeSerializer(instance=instance)
        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()


class TagViewset(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вьюсет для модели тега."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class FavesAndCartViewset(GenericSubscriptionMixin):
    """Вьюсет для избранного и списка покупок."""
    serializer_class = RecipeNestedSerializer
    sub_to_model = Recipe
    url_var = 'recipe_id'

    def get_queryset(self):
        if self.action in ('favorite', 'unfavorite'):
            self.attr_name = 'favorite_recipes'
        elif self.action in (
            'add_to_cart', 'remove_from_cart', 'download_cart'
        ):
            self.attr_name = 'shopping_list'
        return super().get_queryset()

    def favorite(self, request, *args, **kwargs):
        self.attr_name = 'favorite_recipes'
        self.already_subbed_message = 'Уже в избранном.'
        return super().create(request, *args, **kwargs)

    def unfavorite(self, request, *args, **kwargs):
        self.attr_name = 'favorite_recipes'
        self.not_subbed_message = 'Такого рецепта нет в избранном.'
        return super().destroy(request, *args, **kwargs)

    def add_to_cart(self, request, *args, **kwargs):
        self.attr_name = 'shopping_list'
        self.already_subbed_message = 'Уже в списке покупок.'
        return super().create(request, *args, **kwargs)

    def remove_from_cart(self, request, *args, **kwargs):
        self.attr_name = 'shopping_list'
        self.not_subbed_message = 'Такого рецепта нет в списке покупок.'
        return super().destroy(request, *args, **kwargs)

    def download_cart(self, request, *args, **kwargs):
        shopping_list = self.request.user.shopping_list.all()
        sums = shopping_list.values(
            'ingredient_amounts__ingredient__name',
            'ingredient_amounts__ingredient__measurement_unit'
        ).order_by(
            'ingredient_amounts__ingredient__name'
        ).annotate(
            sum=Sum('ingredient_amounts__amount'),
        )
        temp = tempfile.NamedTemporaryFile()
        with open(temp.name, 'w') as file:
            for recipe in shopping_list.order_by('name'):
                file.write(f'{recipe.name}:\n')
                for ingredient in recipe.ingredients.all().order_by('name'):
                    file.write(f' - {ingredient.name}\n')
            file.write('\nИтого необходимо купить:\n')
            for item in sums:
                file.write('{0}: {1} {2}\n'.format(
                    item['ingredient_amounts__ingredient__name'],
                    item['sum'],
                    item['ingredient_amounts__ingredient__measurement_unit'],
                ))
        file_handle = open(temp.name, 'rb')
        response = FileResponse(
            file_handle,
            filename='Shopping-list.txt',
            as_attachment=True,
            content_type='text/plain'
        )
        return response
