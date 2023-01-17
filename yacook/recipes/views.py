from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm, CommentForm
from .models import Group, Recipe, User, Follow


def get_paginator(page_number, recipe):
    """Функция паджинатора."""
    paginator = Paginator(recipe, settings.RECIPE_ON_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    """Главная страница."""
    template = 'recipes/index.html'
    recipes = Recipe.objects.select_related('author', 'group')
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def group_list(request, slug):
    """Страница группы рецептов."""
    template = 'recipes/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    recipes = group.recipes.select_related('author')
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def profile(request, username):
    """Страница профайла пользователя."""
    template = 'recipes/profile.html'
    author = get_object_or_404(User, username=username)
    following = (
        request.user.is_authenticated
        and Follow.objects.filter(author=author, user=request.user).exists()
    )
    recipes = author.recipes.select_related('group')
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'author': author,
        'following': following,
        'page_obj': page_obj,
    }
    return render(request, template, context)


def recipe_detail(request, recipe_id):
    """Страница просмотра рецепта."""
    template = 'recipes/recipe_detail.html'
    recipe = get_object_or_404(Recipe.objects.select_related('author'), pk=recipe_id)
    form = CommentForm()
    comments = recipe.comments.select_related('recipe')
    context = {
        'recipe': recipe,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


@login_required()
def recipe_create(request):
    """Страница добавления нового рецепта пользователем."""
    template = 'recipes/create_recipe.html'
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        return redirect('recipes:profile', recipe.author)
    context = {
        'form': form,
        'is_edit': False
    }
    return render(request, template, context)


@login_required()
def recipe_edit(request, recipe_id):
    """Страница редактирования рецепта."""
    template = 'recipes/create_recipe.html'
    recipe = get_object_or_404(Recipe.objects.select_related('author'), pk=recipe_id)
    if recipe.author != request.user:
        return redirect('recipes:recipe_detail', recipe.id)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )
    if form.is_valid():
        form.save()
        return redirect('recipes:recipe_detail', recipe.id)
    context = {
        'form': form,
        'is_edit': True
    }
    return render(request, template, context)


@login_required
def add_comment(request, recipe_id):
    """Функция для обработки отправленного комментария."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.recipe = recipe
        comment.save()
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)


@login_required
def follow_index(request):
    """Страница с подписками пользователя."""
    template = 'recipes/follow.html'
    recipes = Recipe.objects.filter(author__following__user=request.user)
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {'page_obj': page_obj}
    return render(request, template, context)


@login_required
def profile_follow(request, username):
    """Функция для подписки на автора."""
    author = get_object_or_404(User, username=username)
    if request.user != author:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('recipes:profile', username)


@login_required
def profile_unfollow(request, username):
    """Функция для отписки от автора."""
    author = get_object_or_404(User, username=username)
    Follow.objects.filter(author=author).delete()
    return redirect('recipes:profile', username)
