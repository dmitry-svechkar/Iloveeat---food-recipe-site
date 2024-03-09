from django.core.validators import MinValueValidator
from django.db.models import (CASCADE, SET_NULL, CharField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField,
                              Index, DateTimeField,)
from users.models import User
from recipes.constants import LEN_CONSTANTS as LC


class Recipe(Model):
    author = ForeignKey(
        User, on_delete=SET_NULL,
        related_name='recipes',
        null=True,
        verbose_name='Автор рецепта'
    )
    name = CharField('Название рецепта', max_length=LC['name'])
    image = ImageField('Картинка', upload_to='media/')
    text = TextField('Текстовое описание рецепта')
    ingredients = ManyToManyField(
        'Ingredient',
        through='IngredientQuantity',
        through_fields=('recipe', 'ingredient'),
        related_name='recipes',
        verbose_name='Ингредиенты',
    )
    tags = ManyToManyField(
        'Tag', related_name='recipes',
        verbose_name='Тег'
    )
    cooking_time = PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(
            limit_value=LC['min_value'],
            message='Нельзы указать меньше 1')])
    published = DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return f'Рецепт {self.name}'

    class Meta:
        ordering = ('-published',)
        indexes = [
            Index(fields=['id']),
        ]
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'


class FavoriteRecipes(Model):
    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='favorite_recipes',
        verbose_name='пользователь'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='favorite_recipes',
        verbose_name='Рецепт блюда'
    )

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'

    class Meta:
        verbose_name = 'любимый рецепт'
        verbose_name_plural = 'любимые рецепты'


class ShoppingCart(Model):

    user = ForeignKey(
        User,
        on_delete=CASCADE,
        related_name='shopping_carts',
        verbose_name='пользователь'
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='shopping_carts',
        verbose_name='Рецепт блюда'
    )

    def __str__(self):
        return f'''
            {self.user.username} добавил в
            список покупок рецепт {self.recipe.name}
        '''

    class Meta:
        verbose_name = 'в покупки'
        verbose_name_plural = 'списка покупок'


class Ingredient(Model):
    name = CharField('Название', max_length=LC['name'])
    measurement_unit = CharField(
        'Единицы измерения',
        max_length=LC['ing_unit']
    )

    def __str__(self):
        return f'{self.name} в {self.measurement_unit}'

    class Meta:
        ordering = ('id',)
        indexes = [
            Index(fields=['id'])
        ]
        verbose_name = 'ингридиенты'
        verbose_name_plural = 'ингридиенты'


class IngredientQuantity(Model):
    recipe = ForeignKey(
        Recipe, on_delete=CASCADE,
        related_name='recipe'
    )
    ingredient = ForeignKey(
        Ingredient, on_delete=CASCADE,
        related_name='ingredient'
    )
    amount = PositiveSmallIntegerField(
        'Количество',
        blank=True,
        null=True,
        validators=[MinValueValidator(
            limit_value=LC['min_value'],
            message='Нельзы указать меньше 1')]
    )

    def __str__(self):
        return f'{self.amount} {self.ingredient.name}'

    class Meta:
        verbose_name = 'кол-во ингридиента'
        verbose_name_plural = 'кол-во ингридиентов'


class Tag(Model):
    name = CharField('Название', max_length=LC['name'], unique=True)
    color = CharField('Цветовой код', unique=True, max_length=LC['color_len'])
    slug = SlugField('Слаг', unique=True, max_length=LC['slug_len'])

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'тэг'
        verbose_name_plural = 'тэги'
