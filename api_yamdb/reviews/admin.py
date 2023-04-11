from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'bio', 'role',)
    empty_value_display = '-пусто-'
    list_filter = ('username',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
