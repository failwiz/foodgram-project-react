from django.contrib.auth import get_user_model
from django_filters import rest_framework

from recipes.models import Recipe, Tag


User = get_user_model()


class RecipeFilter(rest_framework.FilterSet):

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    author = rest_framework.ModelChoiceFilter(
        field_name='author',
        queryset=User.objects.all(),
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
        return qs.filter(**filter_kwargs) if value else qs
