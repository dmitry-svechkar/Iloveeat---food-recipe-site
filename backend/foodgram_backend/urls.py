from django.contrib import admin
from django.contrib.auth.models import Group
from django.urls import include, path
from rest_framework.authtoken.models import TokenProxy


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]


admin.site.site_header = 'Администрирование самого лучнего сайта рецептов'
admin.site.site_title = 'Администрирование самого лучнего сайта рецептов'
admin.site.index_title = 'Добро пожалователь в админ-панель'

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)
