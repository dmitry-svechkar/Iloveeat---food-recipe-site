# Generated by Django 4.2.10 on 2024-03-13 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0011_remove_shoppingcart_unique_carts'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='favoriterecipes',
            name='unique_favorite',
        ),
    ]
