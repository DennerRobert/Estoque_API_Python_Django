from django.shortcuts import render

from apps.produto.forms import ProdutosForm
from .models import Produtos
from django.views.generic import UpdateView, View, FormView, ListView, CreateView, DetailView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages


class ProdutoListView(ListView):
    model = Produtos
    template_name = 'produtos_list.html'


class ProdutoAddView(CreateView):
    template_name ='produtos_form.html'
    model = Produtos
    form_class = ProdutosForm
    success_message = 'Produtos adicionado com sucesso'

    def get_context_data(self, **kwargs):
        ctx = super(ProdutoAddView, self).get_context_data(**kwargs)
        return ctx

    def form_valid(self, form):
        produtos_form = form.save(commit=False)
        produtos_form.produto = produtos_form.produto
        produtos_form.preco = produtos_form.preco
        produtos_form.estoque = produtos_form.estoque

        produtos_form.save()
        messages.success(self.request, self.success_message)  
        
        return redirect('produto:produto_add')
    