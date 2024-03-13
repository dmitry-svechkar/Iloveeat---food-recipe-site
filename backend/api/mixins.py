from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND


class GetCreateIsExistsObject:
    """
    Миксин для action функций Subscrive, favorite, shopping_cart.
    """
    def get_user(self, request):
        """ Вспомогательная функция, получающая пользователя запроса. """
        user = request.user
        return user

    def get_obj(self, model, **kwargs):
        """
        Вспомогательная функцмя, получающая объект запроса
        или возвращается None.
        """
        try:
            object = model.objects.get(**kwargs)
        except Exception:
            return None
        return object

    def get_or_create_object(self, model, **kwargs):
        """
        Общий метод для создания объекта по указанной модели.
        """
        object = model.objects.get_or_create(**kwargs)
        return object

    def check_exists(self, object):
        """
        Вспомогательная функция обработки ошибок отсутствия в БД.
        """

        if object is None:
            if self.request.method == 'POST':
                return Response(
                    status=HTTP_400_BAD_REQUEST
                )
            if self.request.method == 'DELETE':
                return Response(
                    status=HTTP_404_NOT_FOUND
                )
