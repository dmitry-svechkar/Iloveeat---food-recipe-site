from django.contrib import admin
from django.utils.safestring import mark_safe

from recipes.models import (FavoriteRecipes, Ingredient, IngredientQuantity,
                            Recipe, ShoppingCart, Tag)


@admin.register(FavoriteRecipes)
class FavoriteRecipesadmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCart(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ('name', 'color', 'slug',)
    list_display = ('name', 'color', 'slug',)
    search_fields = ('name',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    fields = ('name', 'measurement_unit',)
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientQuantityInline(admin.StackedInline):
    model = IngredientQuantity
    autocomplete_fields = ('ingredient',)
    extra = 1
    raw_id_fields = ('ingredient',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ('author', 'name', 'image',
              'read_image', 'text',
              'tags', 'cooking_time',)
    list_display = ('name', 'author', 'total_in_favorite', 'published',)
    list_filter = ('name',)
    search_fields = ('name',)
    readonly_fields = ('read_image', 'total_in_favorite',)
    inlines = (IngredientQuantityInline,)
    filter_vertical = ('ingredients',)

    def read_image(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" style="max-height: 200px;">'
        )
    read_image.short_description = 'Картинка'

    def total_in_favorite(self, obj):

        return obj.favorite_recipes.count()
