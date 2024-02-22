from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        return obj in self.context.get('request').user.favorite_recipes.all()

    def get_is_in_shopping_cart(self, obj):
        return obj in self.context.get('request').user.shopping_list.all()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'text',
            'cooking_time',
        )


class RecipeNestedSerializer(serializers.ModelSerializer):
    """Сериализатор модели рецепта для вкладывания в другие сериализаторы"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
