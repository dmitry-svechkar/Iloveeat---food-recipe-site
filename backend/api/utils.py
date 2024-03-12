from django.db.models import Sum
from recipes.models import IngredientQuantity


def get_user(request):
    """ Вспомогательная функция, получающая пользователя запроса. """
    user = request.user
    return user


def generate_txt_file_with_ingredients(request):
    """
    Функция получения кверисета ингредиентов и записи файла с данными покупок.
    """

    cur_user = get_user(request)
    ingredients = IngredientQuantity.objects.filter(
        recipe__shopping_carts__user=cur_user
    ).values(
        'ingredient__name'
    ).annotate(
        sum=Sum('amount')
    ).values_list(
        'ingredient__name',
        'sum',
        'ingredient__measurement_unit'
    ).order_by('ingredient__name')

    full_path = 'media/shopping_list.txt'
    hello_message = '''
    Привет!
    Ниже список продуктов, которые нужно купить для готовки вкусных блюд!\n\n
    '''
    for ingredient in ingredients:
        name = ingredient[0]
        amount = ingredient[1]
        measurement_unit = ingredient[2]
        if measurement_unit == 'по вкусу':
            amount == ' '

    with open(full_path, 'w+', encoding='utf-8') as file:
        file.write(hello_message)
        for ingredient in ingredients:
            name = ingredient[0]
            amount = ingredient[1]
            measurement_unit = ingredient[2]
            if measurement_unit == 'по вкусу':
                file.write(f'{name} - {measurement_unit}\n')
            else:
                file.write(f'{name} - {amount} - {measurement_unit}\n')
