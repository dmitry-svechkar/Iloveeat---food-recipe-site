from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)


class GetCreateIsExistsObject:
    """
    Миксин для action функций Subscrive, favorite, shopping_cart.
    """
    def get_user(self, request):
        """
        Вспомогательная функция, получающая пользователя запроса.
        """
        user = request.user
        return user

    def create_object(self, request, pk, serializers, model, obj_model, arg):
        """
        Общий метод для создания объекта по указанной модели.
        """
        try:
            obj = obj_model.objects.get(pk=pk)
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)
        else:
            if arg == 'follow_to' and request.user == obj:
                return Response(status=HTTP_400_BAD_REQUEST)
            _, created = model.objects.get_or_create(
                user=request.user, **{arg: obj}
            )
            if not created:
                return Response(status=HTTP_400_BAD_REQUEST)
            serializer = serializers(obj)
            return Response(serializer.data, status=HTTP_201_CREATED)

    def delete_object(self, request, pk, model, obj_model, arg):
        """
        Общий метод для удаления объекта по указанной модели.
        """
        try:
            obj = obj_model.objects.get(pk=pk)
        except Exception:
            return Response(status=HTTP_404_NOT_FOUND)
        else:
            try:
                instance = model.objects.get(
                    user=request.user,
                    **{arg: obj}
                )
            except Exception:
                return Response(status=HTTP_400_BAD_REQUEST)
            else:
                instance.delete()
                return Response(status=HTTP_204_NO_CONTENT)
