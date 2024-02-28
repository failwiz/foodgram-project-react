from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Расширенная модель пользователя, унаследованная от AbstractUser."""

    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        related_name='favoriters',
        verbose_name='Избранное',
    )
    shopping_list = models.ManyToManyField(
        'recipes.Recipe',
        related_name='shoppers',
        verbose_name='Список покупок',
        blank=True,
    )
    subscriptions = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='subscribers',
        verbose_name='Подписки',
        blank=True,
    )

    @property
    def recipes_count(self):
        return self.recipes.count()

    @property
    def generate_shopping_list(self):
        shopping_list = self.shopping_list.all()
        return shopping_list.values(
            'ingredient_amounts__ingredient__name',
            'ingredient_amounts__ingredient__measurement_unit'
        ).order_by(
            'ingredient_amounts__ingredient__name'
        ).annotate(
            sum=models.Sum('ingredient_amounts__amount')
        )
