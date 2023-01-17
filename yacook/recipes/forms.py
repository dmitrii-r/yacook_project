from django import forms

from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    """Форма для добавления нового рецепта."""
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'technology', 'group', 'image')


class CommentForm(forms.ModelForm):
    """Форма для добавления нового комментария."""
    class Meta:
        model = Comment
        fields = ('text',)
