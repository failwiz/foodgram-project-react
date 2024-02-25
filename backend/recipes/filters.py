from django_filters import rest_framework

from recipes.models import Recipe, Tag


class RecipeFilter(rest_framework.FilterSet):

    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ['tags']
