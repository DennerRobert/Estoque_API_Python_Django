from django.shortcuts import render

from apps.produto.forms import ProdutosForm
from .models import Produtos
from django.views.generic import UpdateView, View, FormView, ListView, CreateView, DetailView, DeleteView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.urls import reverse_lazy


class ProdutoListView(ListView):
    model = Produtos
    template_name = 'produtos_list.html'

    def get_context_data(self, **kwargs):
        ctx = super(ProdutoListView, self).get_context_data(**kwargs)
        return ctx

    def get_queryset(self, **kwargs):
        return Produtos.objects.filter(ativo=True).order_by('produto')


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
        produtos_form.ativo = True
        produtos_form.produto = produtos_form.produto
        produtos_form.preco = produtos_form.preco
        produtos_form.estoque = produtos_form.estoque

        produtos_form.save()
        messages.success(self.request, self.success_message)  
        
        return redirect('produto:produto_list')

class ProdutoEditView(UpdateView):
    model = Produtos
    template_name = 'produtos_form.html'
    form_class = ProdutosForm

    def form_valid(self, form):
        produto = form.save()
        messages.success(self.request, 'Produto editado com sucesso!')
        return redirect('produto:produto_list')
    

class DispostivosDeleteAjax(View):
    success_message = 'Dispositivo excluido com sucesso!'
    error_message = 'Ops, Não foi possível excluir o dispositivo!'

    def get(self, request, pk):
        remove_produto = Produtos.objects.filter(pk=pk).first()
        if remove_produto:
            remove_produto.ativo = False
            remove_produto.save()
            messages.success(self.request, self.success_message)  
        else:
            messages.success(self.request, self.error_message) 

        return redirect('produto:produto_list') 
