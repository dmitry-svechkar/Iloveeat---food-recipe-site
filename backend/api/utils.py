from recipes.models import IngredientQuantity, ShoppingCart


def get_user(request):
    """ Вспомогательная функция, получающая пользователя запроса. """
    user = request.user
    return user


def generate_list_of_cart_ingredients(request):
    """
    Функция обработки данных с суммированием одинаковых ингредиентов
    для получения списка покупок.
    """
    cur_user = get_user(request)
    list_of_carts = ShoppingCart.objects.filter(user=cur_user)
    res = {}
    recipes = [item.recipe.id for item in list_of_carts]
    ingredients = [
        item for recipe in recipes
        for item in IngredientQuantity.objects.filter(recipe=recipe)
    ]
    for ingredient in ingredients:
        ingredient_name = ingredient.ingredient.name
        amount = ingredient.amount
        measurement_unit = ingredient.ingredient.measurement_unit
        if ingredient_name not in res:
            if measurement_unit == 'по вкусу':
                res[ingredient_name] = {
                    'amount': None, 'measurement_unit': measurement_unit
                }
            res[ingredient_name] = {
                'amount': amount, 'measurement_unit': measurement_unit
            }
        else:
            if res[ingredient_name]['amount'] is not None:
                res[ingredient_name]['amount'] += amount
    cart_ingredients = [
        {
            'name': name,
            'amount': values['amount'],
            'measurement_unit': values['measurement_unit']
        }
        for name, values in res.items()
        ]
    return cart_ingredients


def generate_txt_file(cart_ingredients, request):
    """ Функция создания и записи файла с данными покупок. """
    full_path = 'media/shopping_list.txt'
    hello_message = '''
    Привет!
    Ниже список продуктов, которые нужно купить для готовки вкусных блюд!\n\n
    '''

    with open(full_path, 'w+', encoding='utf-8') as file:
        file.write(hello_message)
        for ingredient in cart_ingredients:
            name = ingredient['name']
            amount = ingredient['amount']
            quantity = ingredient['measurement_unit']
            if amount is None:
                file.write(f'{name} - {quantity}\n')
            else:
                file.write(f'{name} - {amount} - {quantity}\n')
