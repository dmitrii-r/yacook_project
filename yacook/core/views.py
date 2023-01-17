from django.shortcuts import render


def page_not_found(request, exception):
    """Страница не найдена."""
    return render(request, 'core/404.html', {'path': request.path}, status=404)


def server_error(request):
    """Ошибка сервера."""
    return render(request, 'core/500.html', status=500)


def permission_denied(request, exception):
    """Запрос отклонен."""
    return render(request, 'core/403.html', status=403)


def csrf_failure(request, reason=''):
    """Ошибка CSRF токена."""
    return render(request, 'core/403csrf.html')
