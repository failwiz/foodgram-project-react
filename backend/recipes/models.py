from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        null=False,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
        null=False,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes',
    )
    time_to_cook = models.IntegerField(
        verbose_name='Время приготовления',
    )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Модель тега рецепта."""

    name = models.CharField(
        verbose_name='Название',
        max_length=20,
    ),
    color = models.CharField(
        verbose_name='Цветовой код',
        default='FFFFFF',
        max_length=6,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        null=False,
    )

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        verbose_name='Название',
        max_length=50,
        null=False,
    )

    def __str__(self) -> str:
        return self.name


class Unit(models.Model):
    """Модель единицы измерения для игредиента."""

    name = models.CharField(
        verbose_name='Название',
        max_length=20,
        null=False,
    )
    short_name = models.CharField(
        verbose_name='Сокращение',
        max_length=10,
        null=False,
    )
    base_unit = models.ForeignKey(
        'self',
        verbose_name='Базовая единица',
        on_delete=models.CASCADE,
        null=True,
    )
    coeff = models.FloatField(
        default=1,
        verbose_name='Коэффициент'
    )

    def __str__(self) -> str:
        return self.short_name


class IngredientAmount(models.Model):
    """Модель связи между рецептом и ингредиентом"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        null=False,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        on_delete=models.CASCADE,
        null=False,
    )
    unit = models.ForeignKey(
        Unit,
        verbose_name='Единица измерения',
        on_delete=models.CASCADE,
        null=False,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        null=False,
    )

    def __str__(self) -> str:
        return f'{self.ingredient}, {self.amount} {self.unit}'

    def amount_in_base_unit(self) -> int:
        """Метод для выражения количества ингредиента в базовой единице."""
        return self.amount * self.unit.coeff
