from django.contrib import admin

from .models import Review, Comment, User


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'author',
        'score',
    )
    search_fields = ('pub_date',)
    list_filter = ('pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'review',
        'text',
        'author',
        'Pub_date',
    )
    search_fields = ('review',)
    list_filter = ('review',)


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'bio', 'role',)
    empty_value_display = '-пусто-'
    list_filter = ('username',)
    list_editable = ('role',)


admin.site.register(User, UserAdmin)
