import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag
from users.models import User


class Command(BaseCommand):
    help = 'Импортирует данные из csv в БД'

    def import_users(self):
        with open('data/users.csv', encoding="utf8") as users:
            reader = csv.DictReader(users)
            for row in reader:
                User.objects.create(
                    password=row['password'],
                    is_superuser=row['is_superuser'],
                    username=row['username'],
                    email=row['email'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    is_active=row['is_active'],
                )

    def import_ingredients(self):
        with open('data/ingredients.csv', encoding="utf8") as ingredients:
            reader = csv.DictReader(ingredients)
            for row in reader:
                Ingredient.objects.create(
                    id=row['id'],
                    name=row['name'],
                    measurement_unit=row['measurement_unit'],
                )

    def import_tags(self):
        with open('data/tags.csv', encoding='utf8') as tags:
            reader = csv.DictReader(tags)
            for row in reader:
                Tag.objects.create(
                    name=row['name'],
                    color=row['color'],
                    slug=row['slug'],
                )

    def import_recipe(self):
        with open('data/recipes.csv', encoding='utf8') as recipes:
            reader = csv.DictReader(recipes)
            for row in reader:
                recipe = Recipe.objects.create(
                    author=User.objects.get(id=row['author']),
                    name=row['name'],
                    image=row['image'],
                    text=row['text'],
                    cooking_time=row['cooking_time'],
                )

                tags = [int(tag) for tag in row['tags'].split(',')]
                recipe.tags.set(tags)

    def import_amounts(self):
        with open('data/quantities.csv', encoding='utf8') as quantities:
            reader = csv.DictReader(quantities)
            for row in reader:
                IngredientQuantity.objects.update_or_create(
                    amount=row['amount'],
                    recipe=Recipe.objects.get(id=row['recipe']),
                    ingredient=Ingredient.objects.get(id=row['ingredient'])
                )

    def handle(self, *args, **kwargs):
        try:
            self.import_users()
            self.import_ingredients()
            self.import_tags()
            self.import_recipe()
            self.import_amounts()
        except Exception as error:
            self.stdout.write(self.style.ERROR(error))
        self.stdout.write(self.style.SUCCESS(
            'Данные из CSV файлов успешно загружены!'
        )
        )
