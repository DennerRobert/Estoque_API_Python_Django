from django.shortcuts import render
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

from apps.core.forms import CadastroUsuarioForm


def index(request):
    return render(request, 'index.html')


class CadastroUsuarioView(generic.CreateView):
    model = User
    template_name = 'cadastro.html'
    form_class = CadastroUsuarioForm
    success_url = reverse_lazy('login')