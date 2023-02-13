from django.shortcuts import render
from django.views.generic import UpdateView, View, FormView, ListView, CreateView, DetailView, DeleteView
from .models import Estoque, EstoqueItens
from .forms import EstoqueForm, EstoqueItensForm, EstoqueItensFormSet
from django.shortcuts import redirect
from django.contrib import messages
from django.forms import formset_factory
from django.urls import reverse
from ..produto.models import Produtos
from django.http import JsonResponse

class EstoqueEntradaList(ListView):
    raise_exception = True
    model = Estoque
    template_name = 'estoque_entrada_list.html'

    def get_queryset(self, **kwargs):
        # print('aaaa', Estoque.objects.filter(movimentacao='e').first().__dict__)
        return Estoque.objects.filter(movimentacao='e')


class add_estoque(CreateView):
    template_name ='estoque_entrada_form.html'
    model = Estoque
    form_class = EstoqueForm
    success_message = 'Produtos adicionado com sucesso'

    def get_context_data(self, **kwargs):
        ctx = super(add_estoque, self).get_context_data(**kwargs)
        return ctx

    def form_valid(self, form):
        estoque = form.save(commit=False)
        estoque.movimentacao = 'e'
        estoque.save()
        return redirect('estoque_produtos:estoque_entrada_up', pk=estoque.pk)


class up_estoque(UpdateView):
    template_name ='estoque_entrada_form.html'
    model = Estoque
    form_class = EstoqueForm
    success_message = 'Produtos adicionado com sucesso'

    def get_context_data(self, **kwargs):
        ctx = super(up_estoque, self).get_context_data(**kwargs)
        ctx['estoque_itens_formset'] = EstoqueItensFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        estoque = form.save()

        estoque_itens_formset = EstoqueItensFormSet(self.request.POST, instance=self.object)
        if estoque_itens_formset.is_valid():
            for estoque_item_form in estoque_itens_formset:
                estoque_itens_formset = estoque_item_form.save(commit=False)
                total_produto = Produtos.objects.filter(id = estoque_itens_formset.produto_id).first()
                if total_produto:
                    total_produto.estoque +=  estoque_itens_formset.quantidade
                    total_produto.save()

                estoque_itens_formset.save()

            return redirect('estoque_produtos:estoque_entrada_list')
        
        return redirect('estoque_produtos:estoque_entrada_list')
    

def get_saldo_ajax(request):
    # retomar att saldo
    produto_id = request.GET.get('produto')
    quantidade = request.GET.get('quantidade')

    if not quantidade:
        quantidade = 0
        
    produto = Produtos.objects.filter(id = produto_id).first()
    if produto:
        saldo = int(produto.estoque) + int(quantidade)

    return JsonResponse({'result': saldo})