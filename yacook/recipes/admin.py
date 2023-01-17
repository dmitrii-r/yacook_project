from django.contrib import admin
from .models import Recipe, Group, Comment, Follow


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""
    list_display = ('pk', 'title', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Админка для комментариев"""
    list_display = ('pk', 'text', 'created', 'author', 'recipe')
    list_filter = ('created',)
    empty_value_display = '-пусто-'


admin.site.register(Group)
admin.site.register(Follow)
