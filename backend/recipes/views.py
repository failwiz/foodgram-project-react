from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import (
    mixins,
    ModelViewSet,
    GenericViewSet,
)

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import Ingredient, Recipe, Tag
from recipes.nested import RecipeNestedSerializer
from recipes.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer
)
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
    queryset = Recipe.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = [
        'tags', 'author', 'is_favorited', 'is_in_shopping_list'
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewset(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вьюсет для модели тега."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None


class FavoriteViewset(
    GenericSubscriptionMixin
):

    serializer_class = RecipeNestedSerializer
    sub_to_model = Recipe
    url_var = 'recipe_id'
    attr_name = 'favorite_recipes'

    def get_queryset(self):
        return self.request.user.favorite_recipes.all()


class ShoppingListViewset(
    GenericSubscriptionMixin
):

    serializer_class = RecipeNestedSerializer
    sub_to_model = Recipe
    url_var = 'recipe_id'
    attr_name = 'shopping_list'

    def get_queryset(self):
        return self.request.user.shopping_list.all()
