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

    class Meta:
        model = Recipe
        fields = ['tags', 'author']
