from rest_framework.serializers import ModelSerializer

from recipes.models import Recipe


class RecipeNestedSerializer(ModelSerializer):
    """Сериализатор модели рецепта для вкладывания в другие сериализаторы"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')
