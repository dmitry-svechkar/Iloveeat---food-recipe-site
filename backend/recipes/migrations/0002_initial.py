# Generated by Django 4.2.10 on 2024-03-05 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_carts', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipes.IngredientQuantity', to='recipes.ingredient', verbose_name='Ингредиенты'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', to='recipes.tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient', to='recipes.ingredient'),
        ),
        migrations.AddField(
            model_name='ingredientquantity',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.recipe'),
        ),
        migrations.AddField(
            model_name='favoriterecipes',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to='recipes.recipe', verbose_name='Рецепт блюда'),
        ),
        migrations.AddField(
            model_name='favoriterecipes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to=settings.AUTH_USER_MODEL, verbose_name='пользователь'),
        ),
    ]
