from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm, CommentForm
from .models import Group, Recipe, User, Follow, Comment


def get_paginator(page_number, recipe):
    """Функция паджинатора."""
    paginator = Paginator(recipe, settings.RECIPE_ON_PAGE)
    page_obj = paginator.get_page(page_number)
    return page_obj


def get_groups():
    """Функция получения групп."""
    return Group.objects.values('title', 'slug')


def index(request):
    """Главная страница."""
    template = 'recipes/index.html'
    recipes = Recipe.objects.select_related('author', 'group')
    groups = get_groups()
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'groups': groups,
        'page_obj': page_obj
    }
    return render(request, template, context)


def group_list(request, slug):
    """Страница группы рецептов."""
    template = 'recipes/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    groups = get_groups()
    recipes = group.recipes.select_related('author')
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'groups': groups,
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
    follower = Follow.objects.filter(author=author).aggregate(Count('user'))
    recipes = author.recipes.select_related('group')
    groups = get_groups()
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'author': author,
        'following': following,
        'follower': follower,
        'groups': groups,
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


def search(request):
    """Страница отображения результатов поискового запроса."""
    template = 'recipes/search.html'
    data_search = request.GET.get('s')
    recipes = Recipe.objects.select_related('author', 'group').filter(
        Q(title__iregex=data_search) |
        Q(ingredients__iregex=data_search)
    )
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'data_search': data_search,
        'page_obj': page_obj,
        's': f's={data_search}&'
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


@login_required()
def recipe_delete(request, recipe_id):
    """Функция удаления рецепта пользователем."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    if request.method == 'POST' and request.user == recipe.author:
        recipe.delete()
        return redirect('recipes:profile', request.user)
    return redirect('recipes:recipe_detail', recipe_id)


@login_required
def add_comment(request, recipe_id):
    """Функция для добавления нового комментария."""
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.recipe = recipe
        comment.save()
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)


@login_required
def edit_comment(request, recipe_id, comment_id):
    """Функция для редактирования комментария."""
    # recipe = get_object_or_404(Recipe, pk=recipe_id)
    comment = get_object_or_404(Comment, pk=comment_id)
    form = CommentForm(
        request.POST or None,
        files=request.FILES or None,
        instance=comment
    )
    if form.is_valid():
        # comment = form.save(commit=False)
        # comment.author = request.user
        # comment.recipe = recipe
        comment.save()
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)


@login_required
def delete_comment(request, recipe_id, comment_id):
    """Функция для удаления комментария."""
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST' and request.user == comment.author:
        comment.delete()
    return redirect('recipes:recipe_detail', recipe_id=recipe_id)


@login_required
def follow_index(request):
    """Страница с подписками пользователя."""
    template = 'recipes/follow.html'
    recipes = Recipe.objects.select_related('author', 'group').filter(author__following__user=request.user)
    following = User.objects.all().filter(following__user=request.user)
    groups = get_groups()
    page_number = request.GET.get('page')
    page_obj = get_paginator(page_number, recipes)
    context = {
        'groups': groups,
        'following': following,
        'page_obj': page_obj
    }
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
