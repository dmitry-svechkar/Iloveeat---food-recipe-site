from django.contrib import admin

from users.models import User, UserSubscription


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_active',
        'recipes_count'
    )
    list_filter = ('username', 'email')
    fields = [
        ('username', 'password'),
        ('first_name', 'last_name'),
        'email', 'is_active', 'is_superuser'
    ]
    search_fields = ('username',)
    ordering = ('-date_joined',)

    def recipes_count(self, obj):
        return obj.recipes.count()

    recipes_count.short_description = 'Количество опубликованных рецептов'

    def has_add_permission(self, request):
        return True


@admin.register(UserSubscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = ('follower', 'follow_to')
    list_display = ('follower', 'total_subscribers', 'total_subscriptions',)
    search_fields = ('follower',)

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def get_queryset(self, request):
        return super().get_queryset(
            request
        ).distinct('follower').order_by('follower')

    def total_subscribers(self, obj):
        return obj.follower.follow_to.count()
    total_subscribers.short_description = 'Количество подписчиков'

    def total_subscriptions(self, obj):
        return obj.follow_to.follower.count()
    total_subscriptions.short_description = 'Количество подписок'
