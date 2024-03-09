from django_filters import (CharFilter, FilterSet, ModelChoiceFilter,
                            ModelMultipleChoiceFilter, NumberFilter)
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    """ Фильтрсет по фильтрации полей модели рецептов. """
    is_favorited = NumberFilter(
        method='filter_is_favorited',
        field_name='is_favorited')
    is_in_shopping_cart = NumberFilter(
        method='filter_is_in_card',
        field_name='is_in_shopping_cart')
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
        lookup_expr='contains')
    author = ModelChoiceFilter(queryset=User.objects.all())

    class Meta:
        model = Recipe
        fields = ('tags', 'author',)

    def filter_is_favorited(self, queryset, value, name):
        """ Функция переопределения кверисета по полю is_favorited. """
        if value and self.request.user.is_authenticated:
            user = self.request.user
            queryset = queryset.filter(favorite_recipes__user=user)
        return queryset

    def filter_is_in_card(self, queryset, value, name):
        """ Функция переопределения кверисета по полю is_in_card. """
        if value and self.request.user.is_authenticated:
            user = self.request.user
            queryset = queryset.filter(shopping_carts__user=user)
        return queryset


class IngredientFilter(FilterSet):
    """ Фильтрсет по фильтрации полей модели ингредиентов. """
    name = CharFilter(
        field_name='name',
        lookup_expr='startswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
