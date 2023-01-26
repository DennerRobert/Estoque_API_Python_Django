from django.shortcuts import render
from .models import Produtos
from django.views.generic import DetailView, View, ListView


class ProdutoListView(ListView):
    model = Produtos
    template_name = 'produtos_list.html'
    # objects = Produtos.objects.all()
    # context = {'objects_list': objects}


    # form_class = ModeloLaudoForm