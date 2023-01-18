from django import forms

from .models import Recipe, Comment


class RecipeForm(forms.ModelForm):
    """Форма для добавления нового рецепта."""
    class Meta:
        model = Recipe
        fields = ('title', 'description', 'ingredients', 'technology', 'group', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'ingredients': forms.Textarea(attrs={'rows': 3}),
            'technology': forms.Textarea(attrs={'rows': 3}),
        }


class CommentForm(forms.ModelForm):
    """Форма для добавления нового комментария."""
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
        }
