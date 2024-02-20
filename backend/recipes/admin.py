from django.contrib import admin

from recipes.models import (
        Ingredient,
        IngredientAmount,
        Tag,
        Recipe,
        Unit,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'description',
        'ingredients',
        'tags',
        'time_to_cook',
    )


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
        'unit',
        'amount',
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'short_name',
        'base_unit',
        'cooef',
    )
