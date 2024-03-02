from django.urls import include, path
from recipes.routers import FavesAndCartRouter
from recipes.views import (FavesAndCartViewset, IngredientViewSet,
                           RecipeViewSet, TagViewset)
from rest_framework.routers import DefaultRouter

router_faves_and_cart = FavesAndCartRouter()
router_faves_and_cart.register(
    'recipes', FavesAndCartViewset, 'recipes-additional'
)

router_recipes = DefaultRouter()

basic_endpoints = (
    ('recipes', RecipeViewSet),
    ('ingredients', IngredientViewSet),
    ('tags', TagViewset),
)

for name, viewset in basic_endpoints:
    router_recipes.register(name, viewset, name)

urlpatterns = [
    path('', include(router_faves_and_cart.urls)),
    path('', include(router_recipes.urls)),
]
