from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import CreationForm


class SignUp(CreateView):
    """Страница регистрации нового пользователя."""
    form_class = CreationForm
    success_url = reverse_lazy('recipes:index')
    template_name = 'users/signup.html'
