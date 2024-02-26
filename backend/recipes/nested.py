from rest_framework.serializers import ModelSerializer

from recipes.mixins import GetImageMixin
from recipes.models import Recipe


class RecipeNestedSerializer(ModelSerializer, GetImageMixin):
    """Сериализатор модели рецепта для вкладывания в другие сериализаторы"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
