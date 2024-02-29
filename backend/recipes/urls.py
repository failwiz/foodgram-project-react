from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.routers import FavoriteRouter, ShoppingListRouter
from recipes.views import (
    FavoriteViewset,
    IngredientViewSet,
    RecipeViewSet,
    ShoppingListViewset,
    TagViewset
)


router_faves = ShoppingListRouter()
router_faves.register('recipes', ShoppingListViewset, basename='shopping_cart')

router_cart = FavoriteRouter()
router_cart.register('recipes', FavoriteViewset, basename='favorites')

router_recipes = DefaultRouter()

basic_endpoints = (
    ('recipes', RecipeViewSet),
    ('ingredients', IngredientViewSet),
    ('tags', TagViewset),
)

for name, viewset in basic_endpoints:
    router_recipes.register(name, viewset, name)

urlpatterns = [
    path('', include(router_cart.urls)),
    path('', include(router_faves.urls)),
    path('', include(router_recipes.urls)),
]
