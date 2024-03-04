from django.contrib import admin
from recipes.forms import IngredientAmountFormSet
from recipes.models import Ingredient, IngredientAmount, Recipe, Tag


class IngredientAmountInline(admin.TabularInline):
    formset = IngredientAmountFormSet
    model = Recipe.ingredients.through
    min_num = 1
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'text',
        'cooking_time',
        'favoriters_count',
    )
    inlines = (IngredientAmountInline,)
    exclude = ('ingredients',)
    filter_horizontal = ('tags',)
    search_fields = ('name', 'author__username', 'tags__name')
    list_filter = ('name', 'author__username', 'tags__name')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'measurement_unit'
    )
    search_fields = ('name',)


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
