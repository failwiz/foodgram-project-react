from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    model = User

    filter_horizontal = ('favorite_recipes', 'shopping_list', 'subscriptions')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')
