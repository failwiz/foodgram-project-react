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
