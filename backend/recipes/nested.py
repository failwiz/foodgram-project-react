from django.conf import settings
from django.db.models import Manager
from recipes.mixins import GetImageMixin
from recipes.models import Recipe
from rest_framework.serializers import ListSerializer, ModelSerializer


class NestedRecipeListSerializer(ListSerializer):
    """Кастомный сериализатор для списков."""

    def get_recipes_limit(self):
        """Метод для получения значения query-параметра recipes_limit."""
        limit_recipes = settings.REST_FRAMEWORK['PAGE_SIZE']
        if 'recipes_limit' in self.context.get('request').query_params:
            limit: str = self.context.get(
                'request'
            ).query_params.get('recipes_limit')
            if limit.isdigit():
                limit_recipes = int(limit)
        return limit_recipes

    def to_representation(self, data):
        iterable = data.all()[:self.get_recipes_limit()] if isinstance(
            data, Manager
        ) else data

        return [
            self.child.to_representation(item) for item in iterable
        ]


class RecipeNestedSerializer(ModelSerializer, GetImageMixin):
    """Сериализатор модели рецепта для вкладывания в другие сериализаторы"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        list_serializer_class = NestedRecipeListSerializer
