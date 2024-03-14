from djoser.serializers import UserSerializer as DjoserUserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Ingredient, IngredientQuantity, Recipe, Tag
from rest_framework.serializers import (CharField, ModelSerializer,
                                        PrimaryKeyRelatedField, ReadOnlyField,
                                        SerializerMethodField, ValidationError)
from users.models import User

#  ===========================================================================
#                           Часть пользователя
#  ===========================================================================


class UserSerializer(DjoserUserSerializer):
    """ Класс-сериализатор для модели User. """
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user in obj.followers.all()


class UserSubscribeSerializer(ModelSerializer):
    """
    Класс-сериализатор для модели UserSubscription (Подписки).
    """
    is_subscribed = SerializerMethodField()
    recipes = SerializerMethodField()
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count'
                  )

    def get_is_subscribed(self, obj):
        """ Получение сведений о подписке (True/False). """
        return self.context.get('user') in obj.followers.all()

    def get_recipes(self, obj):
        """ Получение и сериализация данных вложенного get_recipes. """
        recipes = obj.recipes.all()
        serializer = LimitFieldsRecipeSerializer(recipes, many=True)
        return serializer.data

    def get_recipes_count(self, obj):
        """ Получение кол-ва рецептов из запроса. """
        return obj.recipes.count()


#  ===========================================================================
#                           Часть рецепты
#  ===========================================================================


class IsFavoritedAndInShoppingCartMixin:
    """
    Миксин для проверки сведений о избранном и списке покупок.
    """
    def get_is_favorited(self, obj):
        """ Получение сведений о избранном (True/False). """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorite_recipes.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj):
        """ Получение сведений о списке покупок (True/False). """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.shopping_carts.filter(user=user).exists()


class TagSerializer(ModelSerializer):
    """
    Класс-сериализатор для модели Tag.
    """
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class LimitTagRecipe(ModelSerializer):
    """
    Класс-сериализатор для ограничения полей модели Tag.
    """
    class Meta:
        model = Tag
        fields = ('id',)


class IngredientListSerializer(ModelSerializer):
    """ Класс-сериализатор для модели Ingredient. """
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class LimitIngridientCreateSerializer(ModelSerializer):
    """
    Класс-сериализатор для создания и обновления рецептов.
    """
    id = PrimaryKeyRelatedField(
        source='ingredient.id',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = IngredientQuantity
        fields = (
            'id', 'amount',
        )


class IngredientRecipeSerializer(ModelSerializer):
    """
    Класс-сериализатор для получения ингредиентов
    при запросе списка рецептов.
    """
    id = ReadOnlyField(
        source='ingredient.id')
    name = ReadOnlyField(
        source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientQuantity
        fields = (
            'id', 'name', 'measurement_unit', 'amount'
        )


class LimitFieldsRecipeSerializer(ModelSerializer):
    """
    Класс-сериализатор ограничения полей для модели Recipe.
    """
    image = CharField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)


class RecipeSerializer(ModelSerializer, IsFavoritedAndInShoppingCartMixin):
    """Класс-сериализатор для модели Recipe."""
    image = Base64ImageField()
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    ingredients = IngredientRecipeSerializer(
        many=True,
        required=True,
        source='recipe')
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )


class RecipeCreateChangeDeleteSerializer(
    ModelSerializer, IsFavoritedAndInShoppingCartMixin
):
    """
    Класс-сериализатор для модели Recipe(Создание, обновление).
    Логика переопределения входных и выходных данных.
    Логика валидации полей.
    Логика создания и обновления рецептов.
    """
    image = Base64ImageField(required=True)
    ingredients = LimitIngridientCreateSerializer(
        many=True,
        source='recipe')
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserSerializer(read_only=True)
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time'
        )

    def to_representation(self, instance):
        """
        Логика переопределения входных и выходных данных.
        """
        new_representation = super().to_representation(instance)

        tag_ids = new_representation.get('tags', [])
        tag_objects = Tag.objects.filter(id__in=tag_ids)
        tag_serializer = TagSerializer(tag_objects, many=True)
        new_representation['tags'] = tag_serializer.data

        ingredients_data = new_representation.get('ingredients', [])
        transformed_data = []
        for ingredient_data in ingredients_data:
            ingredient_id = ingredient_data['id']
            ingredient = Ingredient.objects.filter(pk=ingredient_id).first()
            transformed_data.append({
                'id': ingredient_id,
                'name': ingredient.name,
                'measurement_unit': ingredient.measurement_unit,
                'amount': ingredient_data['amount']
            })
        new_representation['ingredients'] = transformed_data

        return new_representation

    def validate_image(self, value):
        """ Логика валидации поля image. """
        if not value:
            raise ValidationError('передана пустая строка')
        return value

    def validate_tags(self, value):
        """ Логика валидации поля тегов. """
        if not value:
            raise ValidationError(
                'Необходимо указать как минимум 1 тэг')

        counter_unique_tags = len(set(value))
        counter_of_income_tags = 0
        for _ in value:
            counter_of_income_tags += 1
        if counter_unique_tags != counter_of_income_tags:
            raise ValidationError(
                'Нельзя указывать один и тот же тэг несколько раз')
        return value

    def validate_ingredients(self, value):
        """ Логика валидации поля ингредиентов. """
        if not value:
            raise ValidationError(
                'обязательное поле ingredients'
            )
        unique_ingredients = set()
        counter_of_income_ingredients = 0
        for ingredient in value:
            unique_ingredients.add(ingredient['ingredient']['id'])
            counter_of_income_ingredients += 1
        if len(unique_ingredients) != counter_of_income_ingredients:
            raise ValidationError(
                'Нельзя указывать один и тот же ингредиент несколько раз')
        return value

    def create(self, validated_data):
        """  Логика создания рецептов. """
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('recipe')
        existing_recipe = Recipe.objects.filter(
            name=validated_data['name'],
            text=validated_data['text']
        ).first()
        if existing_recipe:
            raise ValidationError(
                'Рецепт с такими данными уже существует'
            )
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientQuantity.objects.create(
                recipe=recipe,
                ingredient=ingredient['ingredient']['id'],
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        """ Логика  обновления рецептов. """
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time',
            instance.cooking_time
        )
        ingredients = validated_data.get('recipe')
        if not ingredients:
            raise ValidationError(
                'при обновлении рецепта нужно указать минимум 1 ингредиент.'
            )
        clear_flag = False

        for ingredient in ingredients:
            if 'ingredient' in ingredient:
                if not clear_flag:
                    instance.ingredients.clear()
                    clear_flag = True
                IngredientQuantity.objects.create(
                    recipe=instance,
                    ingredient=ingredient['ingredient']['id'],
                    amount=ingredient.get('amount')
                )
        tags = validated_data.get('tags')
        if not tags:
            raise ValidationError(
                'при обновлении рецепта нужно указать минимум 1 тэг.'
            )
        instance.tags.set(tags)
        instance.save()
        return instance
