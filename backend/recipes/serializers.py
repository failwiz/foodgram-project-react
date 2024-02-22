from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    def get_field_names(self, declared_fields, info):
        return (
            self.Meta.short_fields if self.parent
            else super().get_field_names(declared_fields, info)
        )

    class Meta:
        model = Recipe
        fields = '__all__'
        short_fields = ('id', 'name', 'cooking_time')
