import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField(required=False, allow_null=True)

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

    def get_is_favorited(self, obj):
        return obj in self.context.get('request').user.favorite_recipes.all()

    def get_is_in_shopping_cart(self, obj):
        return obj in self.context.get('request').user.shopping_list.all()
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None


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
