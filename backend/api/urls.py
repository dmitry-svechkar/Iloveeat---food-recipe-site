from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api import views

router = DefaultRouter()

router.register('users', views.UserViewSet, basename='user')
router.register('tags', views.TagModelViewSet, basename='tag')
router.register('recipes', views.RecipeViewSet, basename='recipe')
router.register('ingredients', views.IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)),
    path(r'auth/', include('djoser.urls.authtoken')),
]
