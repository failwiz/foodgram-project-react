from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import IngredientViewSet, RecipeViewSet, TagViewset


router = DefaultRouter()

router.register('recipes', RecipeViewSet, 'recipes')
router.register('ingredients', IngredientViewSet, 'ingredients')
router.register('tags', TagViewset, 'tags')

urlpatterns = [
    path('', include(router.urls)),
]
