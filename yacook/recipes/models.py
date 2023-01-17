from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Group(models.Model):
    """Модель для групп рецептов."""
    title = models.CharField(
        verbose_name="Название группы",
        help_text="Укажите название группы",
        max_length=200
    )
    slug = models.SlugField(
        verbose_name="Адрес группы",
        help_text="Укажите адрес группы",
        unique=True
    )
    description = models.TextField(
        verbose_name="Описание группы",
        help_text="Укажите описание группы"
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """Модель для рецептов."""
    title = models.CharField(
        verbose_name="Название рецепта",
        help_text="Укажите название рецепта",
        max_length=200
    )
    description = models.TextField(
        verbose_name="Описание рецепта",
        help_text='Добавьте описание нового рецепта'
    )
    ingredients = models.TextField(
        verbose_name="Ингредиенты",
        help_text='Добавьте ингредиенты нового рецепта'
    )
    technology = models.TextField(
        verbose_name="Технология приготовления",
        help_text='Добавьте технологию приготовления нового рецепта'
    )
    pub_date = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор рецепта",
        help_text="Укажите автора рецепта",
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    group = models.ForeignKey(
        Group,
        verbose_name="Группа",
        help_text='Группа, к которой будет относиться рецепт',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes'
    )
    image = models.ImageField(
        'Изображение готового блюда',
        upload_to='recipes/',
        blank=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Модель для комментариев."""
    recipe = models.ForeignKey(
        Recipe,
        verbose_name="Рецепт",
        help_text='Рецепт, к которому оставлен комментарий',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор комментария",
        help_text="Автор комментария",
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name="Текст комментария",
        help_text='Текст комментария'
    )
    created = models.DateTimeField(
        verbose_name="Дата публикации комментария",
        auto_now_add=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    """Модель подписки на авторов."""
    user = models.ForeignKey(
        User,
        verbose_name="Подписчик",
        help_text='Пользователь, который подписывается',
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        verbose_name="Автор",
        help_text="Пользователь, на которого подписываются",
        on_delete=models.CASCADE,
        related_name='following'
    )

    class Meta:
        verbose_name = "Подписки"
        verbose_name_plural = "Подписки"

    def __str__(self):
        return f"{self.user} подписан на {self.author}"
