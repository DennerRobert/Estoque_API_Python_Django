from django.shortcuts import render
from django.views.generic import UpdateView, View, FormView, ListView, CreateView, DetailView, DeleteView
from .models import Estoque, EstoqueItens


class  EstoqueEntradaList(ListView):
    raise_exception = True
    model = Estoque
    template_name = 'estoque_entrada_list.html'

    def get_queryset(self, **kwargs):
        print('aaaa', Estoque.objects.filter(movimentacao='e').first().__dict__)
        return Estoque.objects.filter(movimentacao='e')