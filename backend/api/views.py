from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings
from djoser.views import UserViewSet
from recipes.models import (FavoriteRecipes, Ingredient, Recipe, ShoppingCart,
                            Tag)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import User, UserSubscription

from api.filters import IngredientFilter, RecipeFilter
from api.mixins import GetCreateIsExistsObject
from api.paginators import StandardPagination, SubPagination
from api.permissions import IsAuthenticatedOrAdminOrAuthor
from api.serializers import (IngredientListSerializer,
                             LimitFieldsRecipeSerializer,
                             RecipeCreateChangeDeleteSerializer,
                             RecipeSerializer, TagSerializer, UserSerializer,
                             UserSubscribeSerializer)

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
        user_subscriptions = UserSubscription.objects.filter(user=user)
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
        methods=['post'],
        detail=True,
        permission_classes=[IsAuthenticated, ]
    )
    def subscribe(self, request, id):
        """ Функция для добавления пользователей  в список подписок."""
        return self.create_object(
            request=request, pk=id,
            serializers=UserSubscribeSerializer,
            model=UserSubscription,
            obj_model=User,
            arg='follow_to'
        )

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        """ Функция для удаления пользователей  из списка подписок."""
        return self.delete_object(
            request=request,
            pk=id,
            model=UserSubscription,
            obj_model=User,
            arg='follow_to'
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

    @action(
        methods=['post'],
        permission_classes=[IsAuthenticated, ],
        detail=True
    )
    def favorite(self, request, pk):
        """ Функция для добавления рецептов в список 'Избранное'."""
        return self.create_object(
            request=request,
            pk=pk,
            serializers=LimitFieldsRecipeSerializer,
            model=FavoriteRecipes,
            obj_model=Recipe,
            arg='recipe'
        )

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        """ Функция для удаления рецептов из списка 'Избранное'."""
        return self.delete_object(
            request=request,
            pk=pk,
            model=FavoriteRecipes,
            obj_model=Recipe,
            arg='recipe'
        )

    @action(
        methods=['post'],
        permission_classes=[IsAuthenticated, ],
        detail=True
    )
    def shopping_cart(self, request, pk):
        """ Функция для добавления рецептов в список покупок."""
        return self.create_object(
            request=request,
            pk=pk,
            serializers=LimitFieldsRecipeSerializer,
            model=ShoppingCart,
            obj_model=Recipe,
            arg='recipe'
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """ Функция для удаления рецептов из список покупок."""
        return self.delete_object(
            request=request,
            pk=pk,
            model=ShoppingCart,
            obj_model=Recipe,
            arg='recipe'
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
