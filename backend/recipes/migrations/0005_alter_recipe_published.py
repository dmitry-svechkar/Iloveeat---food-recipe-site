# Generated by Django 4.2.10 on 2024-03-09 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_alter_ingredient_options_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='published',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации'),
        ),
    ]
