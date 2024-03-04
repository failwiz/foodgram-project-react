from django.contrib.auth import get_user_model
from django.db import models
from recipes.constants import (COLOR_CODE_MAX_LENGTH, INGREDIENT_NAME_LENGTH,
                               MEASUREMENT_MAX_LENGTH, RECIPE_NAME_LENGTH,
                               TAG_NAME_LENGTH)

User = get_user_model()


class Recipe(models.Model):
    """Модель рецепта."""

    name = models.CharField(
        verbose_name='Название',
        max_length=RECIPE_NAME_LENGTH,
        null=False,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes',
    )
    text = models.TextField(
        verbose_name='Описание',
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиенты',
        blank=False,
    )
    tags = models.ManyToManyField(
        'Tag',
        verbose_name='Теги',
        related_name='recipes',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )

    def __str__(self) -> str:
        return self.name

    @property
    def favoriters_count(self):
        return self.favoriters.count()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class Tag(models.Model):
    """Модель тега рецепта."""

    name = models.CharField(
        verbose_name='Название',
        max_length=TAG_NAME_LENGTH,
    )
    color = models.CharField(
        verbose_name='Цветовой код',
        default='FFFFFF',
        max_length=COLOR_CODE_MAX_LENGTH,
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        null=False,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(
        verbose_name='Название',
        max_length=INGREDIENT_NAME_LENGTH,
        null=False,
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=MEASUREMENT_MAX_LENGTH,
        null=False
    )

    def __str__(self) -> str:
        return f'{self.name}, {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class IngredientAmount(models.Model):
    """Модель связи между рецептом и ингредиентом"""

    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredient_amounts',
        on_delete=models.CASCADE,
        null=False,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиент',
        related_name='ingredient_amount',
        on_delete=models.CASCADE,
        null=False,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        null=False,
    )

    def __str__(self) -> str:
        return (f'{self.ingredient.name}, {self.amount} '
                f'{self.ingredient.measurement_unit}')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количества ингредиентов'
