from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """ Типовой пагинатор с переопределением поля queryparam. """
    page_size = 6
    page_size_query_param = 'limit'


class SubPagination(PageNumberPagination):
    """
    Кастомный пагинатор с переопределением поля queryparam.
    Проводится проверка queryparams в запросе на recipes_limit
    с переопределением конечного кверисета.
    Реализован под сущность подписок пользователя.
    """
    page_size_query_param = 'limit'

    def get_page_size(self, request):
        recipes_limit = None
        if 'limit' in request.query_params:
            limit = int(request.query_params['limit'])
            return limit
        if 'recipes_limit' in request.query_params:
            recipes_limit = int(request.query_params['recipes_limit'])
            return recipes_limit
        return self.page_size

    def paginate_queryset(self, queryset, request, view=None):
        recipes_limit = self.get_page_size(request)
        for recipe in queryset:
            recipe['recipes'] = recipe['recipes'][:recipes_limit]
        self.page_size = recipes_limit
        return super().paginate_queryset(queryset, request, view)
