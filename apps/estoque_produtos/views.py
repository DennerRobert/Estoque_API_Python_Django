from django.shortcuts import render
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from .models import Estoque
from .forms import EstoqueForm, EstoqueItensFormSet
from django.shortcuts import redirect
from django.contrib import messages
from ..produto.models import Produtos
from django.http import JsonResponse
from django.forms import inlineformset_factory
from .models import Estoque, EstoqueItens
from .forms import EstoqueForm, EstoqueItensForm
from django.core.paginator import Paginator


class EstoqueEntradaList(ListView):
	raise_exception = True
	model = Estoque
	template_name = 'estoque_entrada_list.html'
	context_object_name = 'entrada'
	paginate_by = 10

	def get_queryset(self, **kwargs):
		return Estoque.objects.filter(movimentacao='e')

	def get_context_data(self, **kwargs):
		ctx = super(EstoqueEntradaList, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Entry'

		entrada = Estoque.objects.filter(movimentacao='e')
		paginator = Paginator(entrada, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['entrada'] = page_obj

		return ctx

class add_estoque(CreateView):
	template_name ='estoque_entrada_form.html'
	model = Estoque
	form_class = EstoqueForm
	success_message = 'Produtos adicionado com sucesso'

	def get_context_data(self, **kwargs):
		ctx = super(add_estoque, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Entry'
		return ctx

	def form_valid(self, form):
		if form.is_valid():
			estoque = form.save(commit=False)
			estoque.movimentacao = 'e'
			estoque.funcionario = self.request.user
			estoque.save()
			return redirect('estoque_produtos:estoque_entrada_up', pk=estoque.pk)
		else:
			print('Error', self.request.user)

class up_estoque(UpdateView):
	template_name ='estoque_entrada_form.html'
	model = Estoque
	form_class = EstoqueForm
	success_message = 'Produtos adicionado com sucesso'

	def get_context_data(self, **kwargs):
		ctx = super(up_estoque, self).get_context_data(**kwargs)
		ctx['estoque_itens_formset'] = EstoqueItensFormSet(instance=self.object)
		ctx['title'] = 'Stock Update'
		return ctx

	def form_valid(self, form):
		estoque = form.save()
		estoque_itens_formset = EstoqueItensFormSet(self.request.POST, instance=self.object)
		
		if estoque_itens_formset.is_valid():
			for estoque_item_form in estoque_itens_formset:
				estoque_itens_formset = estoque_item_form.save(commit=False)
				total_produto = Produtos.objects.filter(id = estoque_itens_formset.produto_id).first()
				
				if total_produto:
					if estoque.movimentacao == 'e':
						total_produto.estoque +=  estoque_itens_formset.quantidade
					else:
						total_produto.estoque -=  estoque_itens_formset.quantidade
					total_produto.save()

				estoque_itens_formset.save()
			
			if estoque.movimentacao == 'e':
				return redirect('estoque_produtos:estoque_entrada_list')
			else:
				return redirect('estoque_produtos:estoque_saida_list')
		else:
			print('Formset errors:', estoque_itens_formset.errors)

		if estoque.movimentacao == 'e':
			return redirect('estoque_produtos:estoque_entrada_list')
		else:
			return redirect('estoque_produtos:estoque_saida_list')

class EstoqueSaidaList(ListView):
	raise_exception = True
	model = Estoque
	template_name = 'estoque_saida_list.html'
	context_object_name = 'saida'
	paginate_by = 10

	def get_queryset(self, **kwargs):
		return Estoque.objects.filter(movimentacao='s')  

	def get_context_data(self, **kwargs):
		ctx = super(EstoqueSaidaList, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Exit'

		saida = Estoque.objects.filter(movimentacao='s')
		paginator = Paginator(saida, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['saida'] = page_obj

		return ctx 

class del_estoque(CreateView):
	template_name ='estoque_entrada_form.html'
	model = Estoque
	form_class = EstoqueForm
	success_message = 'Produtos retirado com sucesso'

	def get_context_data(self, **kwargs):
		ctx = super(del_estoque, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Exit'
		return ctx

	def form_valid(self, form):
		estoque = form.save(commit=False)
		estoque.movimentacao = 's'
		estoque.funcionario = self.request.user
		estoque.save()
		return redirect('estoque_produtos:estoque_entrada_up', pk=estoque.pk)

#Atualizar saldo em tela -
def produto_saldo(request, produto_id):
	produto = Produtos.objects.filter(id = produto_id).first()
	saldo_disponivel = produto.preco
	return JsonResponse({'saldo_disponivel': saldo_disponivel})

# detail entry product
class Detail_stock_entry(ListView):
	template_name = 'detail_entry_list.html'
	model = Estoque
	form_class = EstoqueForm

	def get_context_data(self, **kwargs):
		ctx = super(Detail_stock_entry, self).get_context_data(**kwargs)
		id = self.kwargs.get('pk')
		product = Estoque.objects.filter(id=id).first()

		EstoqueItensFormSet = inlineformset_factory(Estoque, EstoqueItens, form=EstoqueItensForm, extra=0)

		ctx['estoque'] = product
		ctx['user'] = product.funcionario
		ctx['nf'] = product.nf
		ctx['movimentacao'] = product.movimentacao
		ctx['formset'] = EstoqueItensFormSet(instance=product)
		ctx['title'] = 'Detail Entry'

		# Passa os dados de cada formulário individualmente para o contexto
		if EstoqueItensFormSet(instance=product):
			for form in EstoqueItensFormSet(instance=product):
				produto_nome = form.instance.produto.produto if form.instance.produto else ''

				ctx['produto_nome'] = produto_nome
		
		return ctx
	
# detail entry product
class Detail_stock_exit(ListView):
	template_name = 'detail_exit_list.html'
	model = Estoque
	form_class = EstoqueForm

	def get_context_data(self, **kwargs):
		ctx = super(Detail_stock_exit, self).get_context_data(**kwargs)
		id = self.kwargs.get('pk')
		product = Estoque.objects.filter(id=id).first()

		EstoqueItensFormSet = inlineformset_factory(Estoque, EstoqueItens, form=EstoqueItensForm, extra=0)

		ctx['estoque'] = product
		ctx['user'] = product.funcionario
		ctx['nf'] = product.nf
		ctx['movimentacao'] = product.movimentacao
		ctx['formset'] = EstoqueItensFormSet(instance=product)
		ctx['title'] = 'Detail Exit'

		# Passa os dados de cada formulário individualmente para o contexto
		if EstoqueItensFormSet(instance=product):
			for form in EstoqueItensFormSet(instance=product):
				produto_nome = form.instance.produto.produto if form.instance.produto else ''

				ctx['produto_nome'] = produto_nome
		
		return ctx