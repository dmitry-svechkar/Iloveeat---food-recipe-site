# Generated by Django 4.2.10 on 2024-03-06 16:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=100, verbose_name='Имя пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='\n            Поставьте галочку, если хотите\n            сделать этого пользователя администратором\n        ', verbose_name='Администратор'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, verbose_name='Фамилия пользователя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+\\Z')], verbose_name='Ник-нейм'),
        ),
    ]
