from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from .constants import MIN_FIELD_VALUE, MAX_FIELD_VALUE

User = get_user_model()


class Tag(models.Model):
    """Модель тегов для рецептов."""
    name = models.CharField(verbose_name='Тег', max_length=200)
    color = ColorField(
        verbose_name='Цветовой код',
        default='#00FF00',
        format='hex',
        unique=True
    )
    slug = models.SlugField(verbose_name='Слаг тега', unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель ингредиентов для рецепта."""
    name = models.CharField(verbose_name='Ингредиент', max_length=256)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=24
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(models.Model):
    """Модель для рецептов."""
    name = models.CharField(
        verbose_name='Название',
        max_length=256
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='recipes'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(verbose_name='Описание', max_length=5000)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[
            MinValueValidator(MIN_FIELD_VALUE),
            MaxValueValidator(MAX_FIELD_VALUE)
        ]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class RecipeIngredient(models.Model):
    """Модель для связывания количества ингредиентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='recipe_ingredient',
        verbose_name='Ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name='recipe_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(MIN_FIELD_VALUE),
            MaxValueValidator(MAX_FIELD_VALUE)
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'
        constraints = (
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredients_recipe'),
        )
        ordering = ['id']

    def __str__(self):
        return f'{self.ingredient} - {self.recipe} - {self.amount}'


class Favorite(models.Model):
    """Модель для избранных рецептов пользователя."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    user = models.ForeignKey(
        User,
        related_name='favorites',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = (
            models.UniqueConstraint(
                name='%(app_label)s_%(class)s_unique_relationships',
                fields=('recipe', 'user'),
            ),
        )
        ordering = ['id']

    def __str__(self):
        return f'{self.user}/{self.recipe}'


class ShoppingCart(models.Model):
    """Модель для списка покупок пользователя."""
    recipe = models.ForeignKey(
        Recipe,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        related_name='cart',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_user_recipe_in_cart'),
        )
        ordering = ['id']

    def __str__(self):
        return f'{self.user} / {self.recipe}'
