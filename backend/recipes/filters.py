from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters import rest_framework

from recipes.models import Ingredient, Recipe, Tag


User = get_user_model()


class RecipeFilter(rest_framework.FilterSet):
    """Набор фильтров для модели рецепта."""

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    author = rest_framework.CharFilter(
        field_name='author',
        method='filter_author'
    )
    is_favorited = rest_framework.BooleanFilter(
        field_name='favoriters',
        method='filter_is_favorited',
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        field_name='shoppers',
        method='filter_is_favorited',
    )

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_favorited', 'is_in_shopping_cart']

    def filter_is_favorited(self, qs, name, value):
        filter_kwargs = {
            '{}'.format(name): self.request.user
        }
        return qs.filter(**filter_kwargs) if (
            value and self.request.user.is_authenticated
        ) else qs

    def filter_author(self, qs, name, value: str):
        if value == 'me':
            return qs.filter(author__id=self.request.user.id)
        return qs.filter(author__id=int(value)) if value.isdigit() else qs


class IngredientFilter(rest_framework.FilterSet):
    """Набор фильтров для модели ингредиента."""

    name = rest_framework.CharFilter(
        method='filter_name',
        field_name='name',
    )

    class Meta:
        model = Ingredient
        fields = ['name']

    def filter_name(self, qs, name, value):
        filter_kwargs_start = {
            '{0}__{1}'.format(name, 'istartswith'): value,
        }
        filter_kwargs_contains = {
            '{0}__{1}'.format(name, 'icontains'): value,
        }

        return qs.filter(
            Q(**filter_kwargs_start) | Q(**filter_kwargs_contains)
        ) if value else qs
