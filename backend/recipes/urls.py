from django.urls import include, path
from rest_framework.routers import DefaultRouter, Route, SimpleRouter

from recipes.views import (
    FavoriteViewset,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListViewset,
    TagViewset
)


class FavoriteRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/favorite/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='favorites',
            detail=False,
            initkwargs={}
        ),
    ]


class ShoppingListRouter(SimpleRouter):
    """Маршрутизатор для кастомных эндпойнтов для подписок."""

    routes = [
        Route(
            url=r'^{prefix}/download_shopping_cart/$',
            mapping={'get': 'download'},
            name='download_shopping_cart',
            detail=False,
            initkwargs={}
        ),
        Route(
            url=r'^{prefix}/(?P<recipe_id>\d+)/shopping_cart/$',
            mapping={'post': 'create', 'delete': 'destroy'},
            name='shopping_cart',
            detail=False,
            initkwargs={}
        ),
    ]


router_faves = ShoppingListRouter()
router_faves.register('recipes', ShoppingListViewset, basename='cart')

router_cart = FavoriteRouter()
router_cart.register('recipes', FavoriteViewset, basename='faves')

router_recipes = DefaultRouter()

router_recipes.register('recipes', RecipeViewSet, 'recipes')
router_recipes.register('ingredients', IngredientViewSet, 'ingredients')
router_recipes.register('tags', TagViewset, 'tags')

urlpatterns = [
    path('', include(router_cart.urls)),
    path('', include(router_faves.urls)),
    path('', include(router_recipes.urls)),
]
