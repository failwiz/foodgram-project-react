from rest_framework import serializers

from users.serializers import CustomUserSerializer
from recipes.mixins import (
    GetImageMixin,
    IsFavoritedMixin,
    isInShoppingCartMixin
)
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор количества ингредиента."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(
    serializers.ModelSerializer,
    GetImageMixin,
    IsFavoritedMixin,
    isInShoppingCartMixin
):
    """Сериализатор для модели рецепта."""

    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts'
    )
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    tags = TagSerializer(many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

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
            'image',
            'text',
            'cooking_time',
        )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amounts')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            recipe.tags.add(tag)
        for element in ingredients:
            ingredient = element['ingredient']
            amount = element['amount']
            recipe.ingredients.add(
                ingredient,
                through_defaults={'amount': amount}
            )
        return recipe
