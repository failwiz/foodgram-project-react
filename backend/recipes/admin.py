from django.contrib import admin

from recipes.models import (
        Ingredient,
        IngredientAmount,
        Tag,
        Recipe,
)


class IngredientAmountInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'description',
        'cooking_time',
    )
    inlines = (IngredientAmountInline,)
    exclude = ('ingredients',)
    filter_horizontal = ('tags',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'color',
        'slug',
    )


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):

    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
