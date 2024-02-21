from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.db.models.constraints import UniqueConstraint, CheckConstraint


class CustomUser(AbstractUser):
    """Расширенная модель пользователя, унаследованная от AbstractUser."""

    favorite_recipes = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        verbose_name='Избранное',
    )
    shopping_list = models.ManyToManyField(
        'recipes.IngredientAmount',
        related_name='shoppers',
        verbose_name='Список покупок',
        blank=True,
    )


User = get_user_model()


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='subscribed_to',
    )
    subscription = models.ForeignKey(
        User,
        verbose_name='Подписка',
        on_delete=models.CASCADE,
        related_name='subscribers',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

        constraints = [
            UniqueConstraint(
                fields=['user', 'subscription'],
                name='unique_user_following'
            ),
            CheckConstraint(
                check=~Q(user__exact=F('subscription')),
                name='not_following_self'
            )
        ]
