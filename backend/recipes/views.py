from rest_framework.viewsets import (
    mixins,
    ModelViewSet,
    GenericViewSet,
)

from recipes.models import Ingredient, Recipe, Tag
from recipes.serializers import (
    IngredientSerializer,
    RecipeNestedSerializer,
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


class RecipeViewSet(ModelViewSet):
    """Вьюсет для модели рецепта."""

    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class TagViewset(
    GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вьюсет для модели тега."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class FavoriteViewset(
    GenericSubscriptionMixin
):

    serializer_class = RecipeNestedSerializer
    sub_to_model = Recipe
    url_var = 'recipe_id'
    attr_name = 'favorite_recipes'

    def get_queryset(self):
        return self.request.user.favorite_recipes


class ShoppingListViewset(
    GenericSubscriptionMixin
):

    serializer_class = RecipeNestedSerializer
    sub_to_model = Recipe
    url_var = 'recipe_id'
    attr_name = 'shopping_list'

    def get_queryset(self):
        return self.request.user.shopping_list
