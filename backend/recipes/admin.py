from django.contrib import admin

from recipes.models import (
        Ingredient,
        IngredientAmount,
        Tag,
        Recipe,
        Unit,
        UnitKind,
)


class IngredientAmountInline(admin.TabularInline):
    model = Recipe.ingredients.through


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'description',
        'time_to_cook',
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
        'unit',
        'amount',
    )


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'short_name',
        'unit_kind',
        'base_unit',
        'coeff',
    )


@admin.register(UnitKind)
class UnitKindAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )
