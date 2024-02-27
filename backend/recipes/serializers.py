from rest_framework.serializers import (
    CurrentUserDefault,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    SerializerMethodField,
)

from users.serializers import CustomUserSerializer
from recipes.mixins import (
    Base64ImageField,
    GetImageMixin,
    IsFavoritedMixin,
    isInShoppingCartMixin
)
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientSerializer(ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(ModelSerializer):
    """Сериализатор количества ингредиента."""

    id = PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient',
    )
    name = SerializerMethodField()
    measurement_unit = SerializerMethodField()
    amount = IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount', 'name', 'measurement_unit')

    def get_name(self, obj):
        return obj.ingredient.name

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit


class TagSerializer(ModelSerializer):
    """Сериализатор модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeCreateUpdateSerializer(
    ModelSerializer,
    GetImageMixin,
    IsFavoritedMixin,
    isInShoppingCartMixin
):
    """Сериализатор для модели рецепта (создание/редактирование)."""

    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts',
    )
    author = CustomUserSerializer(
        read_only=True,
        default=CurrentUserDefault()
    )
    tags = PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    image = Base64ImageField(required=True, allow_null=True)

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def assign_ingredient_amounts(self, recipe, ingredients):
        for ingredient in ingredients:
            if ingredient['ingredient'] not in recipe.ingredients.all():
                IngredientAmount.objects.update_or_create(
                    recipe=recipe, **ingredient
                )
            else:
                cur_amount = recipe.ingredient_amounts.get(
                    ingredient=ingredient['ingredient']
                )
                cur_amount.amount += ingredient['amount']
                cur_amount.save()
        return recipe

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredient_amounts')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.assign_ingredient_amounts(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        new_ingredients = validated_data.pop('ingredient_amounts')
        new_tags = validated_data.pop('tags')
        for field in validated_data:
            setattr(instance, field, validated_data[field])
        instance.tags.set(new_tags)
        instance.ingredients.clear()
        self.assign_ingredient_amounts(instance, new_ingredients)
        return instance


class RecipeSerializer(
    ModelSerializer,
    GetImageMixin,
    IsFavoritedMixin,
    isInShoppingCartMixin
):
    """Сериализатор для модели рецепта."""

    ingredients = IngredientAmountSerializer(
        many=True,
        source='ingredient_amounts'
    )
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField(required=True, allow_null=True)

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


class DownloadShoppingListSerializer(Serializer):
    """Сериализатор для скачивания списка покупок."""

    field = SerializerMethodField()

    class Meta:
        fields = ('field',)

    def get_field(self, obj):
        return 'test?'
