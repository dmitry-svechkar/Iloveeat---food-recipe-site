from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from recipes.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                            Tag)
from users.models import User, UserSubscription

from api.filters import IngredientFilter, RecipeFilter
from api.paginators import StandardPagination, SubPagination
from api.permissions import IsAuthenticatedOrAdminOrAuthor
from api.serializers import (IngredientListSerializer,
                             LimitFieldsRecipeSerializer,
                             RecipeCreateChangeDeleteSerializer,
                             RecipeSerializer, TagSerializer, UserSerializer,
                             UserSubscribeSerializer)
from api.mixins import GetCreateIsExistsObject

#  ===========================================================================
#                           Часть пользователя
#  ===========================================================================


class UserViewSet(GetCreateIsExistsObject, UserViewSet):
    """
    Класс-представление для работы моделью Recipe.
    Определены несколько @action функций с
    распределенной логикой.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardPagination

    def get_permissions(self):
        """
        Функция переопределения экшена 'me'
        из стандартного viewset djoser.
        """
        if self.action == 'me':
            self.permission_classes = settings.PERMISSIONS.me
        return super().get_permissions()

    def pagination_class(self):
        """
        Функция-переопределить пагинатора в зависимости
        от экшена пользователя.
        """
        if self.action in ['subscriptions', 'subscribe']:
            return SubPagination()
        else:
            return StandardPagination()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated, ]
    )
    def subscriptions(self, request):
        """ Функция для получения списка отслеживаемых авторов."""
        user = self.get_user(request)
        user_subscriptions = UserSubscription.objects.filter(follower=user)
        follow_to_users = [
            subscription.follow_to for subscription in user_subscriptions
        ]
        serializer = UserSubscribeSerializer(
            follow_to_users,
            many=True,
            context={'user': user}
        )
        paginated_data = self.paginator.paginate_queryset(
            serializer.data,
            request
        )
        return self.paginator.get_paginated_response(paginated_data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, id=None):
        """ Функция для добавления пользователей  в список отслеживаемых."""
        follow_to = self.get_obj(User, id=id)
        is_follow_to_exists = self.check_exists(follow_to)
        if is_follow_to_exists:
            return is_follow_to_exists
        if self.request.method == 'POST':
            if self.get_user(request) == follow_to:
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )
            instance, created = self.get_or_create_object(
                UserSubscription,
                follower=self.get_user(request),
                follow_to=follow_to
            )
            if not created:
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )
            serializer = UserSubscribeSerializer(follow_to)
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        if self.request.method == 'DELETE':
            instance = self.remove_object(
                UserSubscription,
                follower=self.get_user(request),
                follow_to=follow_to
            )
            if instance:
                return Response(status=HTTP_204_NO_CONTENT)
            return Response(
                status=HTTP_400_BAD_REQUEST
            )

#  ===========================================================================
#                           Часть рецепты
#  ===========================================================================


class TagModelViewSet(viewsets.ModelViewSet):
    """ Класс-представление для работы  с моделью Tag."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    http_method_names = ['get', ]


class IngredientViewSet(viewsets.ModelViewSet):
    """ Класс-представление для работы  с моделью Ingredient. """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientListSerializer
    pagination_class = None
    filterset_class = IngredientFilter
    http_method_names = ['get', ]


class RecipeViewSet(GetCreateIsExistsObject, viewsets.ModelViewSet):
    """
    Класс-представление для работы моделью Recipe.
    Определены несколько @action функций с
    распределенной логикой.
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [
        IsAuthenticatedOrAdminOrAuthor,
    ]
    pagination_class = StandardPagination
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        """
        Функция-заполнения поля автора рецепта после сериализации.
        """
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        """
        Функция - определитель сериализатора в зависимости от типа запроса.
        """
        if self.request.method == 'GET':
            return RecipeSerializer
        return RecipeCreateChangeDeleteSerializer

    def get_recipe(self, request, pk=None):
        """ Вспомогательная функция для получения объекта рецепта. """
        try:
            recipe = Recipe.objects.get(id=pk)
        except Exception:
            return None
        return recipe

    @action(
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        detail=True
    )
    def favorite(self, request, pk):
        """ Функция для добавления рецептов в список "Избранное"."""
        recipe = self.get_obj(Recipe, id=pk)
        is_recipe_exists = self.check_exists(recipe)
        if is_recipe_exists:
            return is_recipe_exists
        if self.request.method == 'POST':
            instance, created = self.get_or_create_object(
                FavoriteRecipes,
                user=self.get_user(request),
                recipe=recipe
            )
            if not created:
                return Response(
                    {'error': 'Этот рецепт уже в избранном.'},
                    status=HTTP_400_BAD_REQUEST
                )
            serializer = LimitFieldsRecipeSerializer(recipe)
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        if self.request.method == 'DELETE':
            instance = self.remove_object(
                FavoriteRecipes,
                user=self.get_user(request),
                recipe=recipe
            )
            if instance:
                return Response(status=HTTP_204_NO_CONTENT)
            return Response(
                status=HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated, ],
        detail=True
    )
    def shopping_cart(self, request, pk=None):
        """ Функция для добавления рецептов в список покупок."""
        recipe = self.get_obj(Recipe, id=pk)
        is_recipe_exists = self.check_exists(recipe)
        if is_recipe_exists:
            return is_recipe_exists
        if self.request.method == 'POST':
            instance, created = self.get_or_create_object(
                ShoppingCart,
                user=self.get_user(request),
                recipe=recipe
            )
            if not created:
                return Response(
                    {'error': 'Этот рецепт уже в списке покупок.'},
                    status=HTTP_400_BAD_REQUEST
                )
            serializer = LimitFieldsRecipeSerializer(recipe)
            return Response(
                serializer.data, status=HTTP_201_CREATED
            )
        if self.request.method == 'DELETE':
            instance = self.remove_object(
                ShoppingCart,
                user=self.get_user(request),
                recipe=recipe
            )
            if instance:
                return Response(status=HTTP_204_NO_CONTENT)
            return Response(
                status=HTTP_400_BAD_REQUEST
            )

    @action(
        methods=['get'],
        permission_classes=[IsAuthenticated],
        detail=False
    )
    def download_shopping_cart(self, request):
        """
        Функция для реализации скачивания списка ингридиентов
        в формате ".txt".
        Реализована логика расчета, повторяющихся ингридиентов,
        В случае если мера измерения - "по вкусу", значение в итоговом
        варианте пропускается.
        Получается пример "Авокадо - по вкусу".
        """
        from api.utils import generate_txt_file_with_ingredients

        generate_txt_file_with_ingredients(request)
        file_path = 'media/shopping_list.txt'
        response = FileResponse(
            open(file_path, 'rb'), content_type='text/plain'
        )
        response[
            'Content-Disposition'
        ] = 'attachment; filename="shopping_list.txt"'
        return response
