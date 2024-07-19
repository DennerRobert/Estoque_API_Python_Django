from django.shortcuts import get_object_or_404, render
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from .forms import InventoryForm, InventoryItemsFormSet, InventoryItemsForm
from django.shortcuts import redirect
from django.contrib import messages
from ..produto.models import Products
from django.http import JsonResponse
from django.forms import inlineformset_factory
from .models import Inventory, InventoryItems
from django.core.paginator import Paginator


# Listar todos os itens do estoque
class StockEntryListView(ListView):
	raise_exception = True
	model = Inventory
	template_name = 'stock_entry_list.html'
	context_object_name = 'entries'
	paginate_by = 10

	# Filtrar apenas as entradas
	def get_queryset(self, **kwargs):
		return Inventory.objects.filter(movement='e')

	# Páginação do resultado
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['title'] = 'Stock Entries'

		entries = Inventory.objects.filter(movement='e')
		paginator = Paginator(entries, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['entries'] = page_obj

		return ctx
	

# Criar um formulário para adicionar entradas de produtos ao estoque
class StockEntryCreateView(CreateView):
	template_name = 'stock_entry_form.html'
	model = Inventory
	form_class = InventoryForm
	success_message = 'Product added successfully'

	# Pegar os dados do formulário e preencher o formulário
	def get_context_data(self, **kwargs):
		ctx = super(StockEntryCreateView, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Entries'
		return ctx

	#  Salvar os dados do formulário
	def form_valid(self, form):
		if form.is_valid():
			stock_entry = form.save(commit=False)
			stock_entry.movement = 'e'
			stock_entry.employee = self.request.user
			stock_entry.save()
			return redirect('estoque_produtos:stock_update', pk=stock_entry.pk)
		else:
			print('Error', self.request.user)


# Atualizar um formulário para adicionar entradas/saídas de produtos ao estoque
class StockUpdateView(UpdateView):
	template_name ='stock_entry_form.html'
	model = Inventory
	form_class = InventoryForm
	success_message = 'Produtos atualizados com sucesso'
	# Pegar os dados do formulário e preencher o formulário	
	def get_context_data(self, **kwargs):
		ctx = super(StockUpdateView, self).get_context_data(**kwargs)
		if self.object:
			ctx['estoque_itens_formset'] = InventoryItemsFormSet(instance=self.object)
		else:
			ctx['estoque_itens_formset'] = InventoryItemsFormSet()
		ctx['title'] = 'Stock Update'
		return ctx
	# Salvar os dados do formulário
	def form_valid(self, form):
		stock = form.save(commit=False)
		stock_items_formset = InventoryItemsFormSet(self.request.POST, instance=stock)
		# Verificar se todos os formulários estão válidos
		if stock_items_formset.is_valid():
			stock_item_form = stock_items_formset.forms[0]
			stock_item = stock_item_form.save(commit=False)
			
			# Atualizar o estoque e os itens
			stock_item_current  = None
			if stock_item.id:
				stock_item_current  = InventoryItems.objects.get(id=stock_item.id)
			
			if stock_item_current  and stock_item.product_id != stock_item_current.product_id:
				old_product = get_object_or_404(Products, id=stock_item_current.product_id)
				new_product = get_object_or_404(Products, id=stock_item.product_id)
				
				if stock.movement == 'e':
					old_product.inventory -= stock_item_current.quantity
					new_product.inventory += stock_item.quantity
				
				elif stock.movement == 's':
					old_product.inventory += stock_item_current.quantity
					new_product.inventory -= stock_item.quantity

				old_product .save()
				new_product.save()

			else:
				for stock_item_form in stock_items_formset:
					stock_items_formset = stock_item_form.save(commit=False)
					total_product = Products.objects.filter(id = stock_items_formset.product_id).first()
					
					if total_product:
						if stock.movement == 'e':
							total_product.inventory +=  stock_items_formset.quantity
						else:
							total_product.inventory -=  stock_items_formset.quantity
						total_product.save()

					stock_items_formset.save()
			stock_item.save()
			stock.save()

			if stock.movement == 'e':
				return redirect('estoque_produtos:stock_entry_list')
			else:
				return redirect('estoque_produtos:stock_output_list')
		else:
			print('Formset errors:', stock_items_formset.errors)

		return super().form_invalid(form)


# Remover um formulário para dar saída produtos do estoque
class StockOutputListView(ListView):
	raise_exception = True
	model = Inventory
	template_name = 'stock_output_list.html'
	context_object_name = 'output'
	paginate_by = 10
	# Filtrar apenas as saídas
	def get_queryset(self, **kwargs):
		return Inventory.objects.filter(movement='s')  
	# Páginação do resultado
	def get_context_data(self, **kwargs):
		ctx = super(StockOutputListView, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Exits'

		output = Inventory.objects.filter(movement='s')
		paginator = Paginator(output, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['output'] = page_obj

		return ctx 

class StockOutputCreateView(CreateView):
	template_name = 'stock_exit_form.html'
	model = Inventory
	form_class = InventoryForm
	success_message = 'Products successfully removed'

	# Pegar os dados do formulário e preencher o formulário	
	def get_context_data(self, **kwargs):
		ctx = super(StockOutputCreateView, self).get_context_data(**kwargs)
		ctx['title'] = 'Stock Exits'
		
		return ctx
	
	# Salvar os dados do formulário
	def form_valid(self, form):
		stock_output = form.save(commit=False)
		stock_output.movement = 's'
		stock_output.employee = self.request.user
		stock_output.save()
		
		return redirect('estoque_produtos:stock_update', pk=stock_output.pk)


# Atualizar saldo em tela
def produto_saldo(request, produto_id):
	produto = Products.objects.filter(id = produto_id).first()
	saldo_disponivel = produto.price
	
	return JsonResponse({'saldo_disponivel': saldo_disponivel})


# Detalhes de entrada de produtos
class StockEntryDetailView(ListView):
	template_name = 'stock_entry_detail.html'
	model = Inventory
	form_class = InventoryForm

	def get_context_data(self, **kwargs):
		ctx = super(StockEntryDetailView, self).get_context_data(**kwargs)
		id = self.kwargs.get('pk')
		product = Inventory.objects.filter(id=id).first()

		InventoryItemsFormSet = inlineformset_factory(Inventory, InventoryItems, form=InventoryItemsForm, extra=0)

		ctx['product'] = product
		ctx['user'] = product.employee
		ctx['invoice_number'] = product.invoice_number
		ctx['movement'] = product.movement
		ctx['formset'] = InventoryItemsFormSet(instance=product)
		ctx['title'] = 'Detail Entry'

		# Passa os dados de cada formulário individualmente para o contexto
		if InventoryItemsFormSet(instance=product):
			for form in InventoryItemsFormSet(instance=product):
				produto_nome = form.instance.product.product if form.instance.product else ''

				ctx['produto_nome'] = produto_nome
		
		return ctx
	

# Detalhes de saída de produtos
class StockOutputDetailView(ListView):
	template_name = 'stock_output_detail.html'
	model = Inventory
	form_class = InventoryForm

	def get_context_data(self, **kwargs):
		ctx = super(StockOutputDetailView, self).get_context_data(**kwargs)
		id = self.kwargs.get('pk')
		product = Inventory.objects.filter(id=id).first()

		EstoqueItensFormSet = inlineformset_factory(Inventory, InventoryItems, form=InventoryItemsForm, extra=0)

		ctx['product'] = product
		ctx['user'] = product.employee
		ctx['invoice_number'] = product.invoice_number
		ctx['movement'] = product.movement
		ctx['formset'] = InventoryItemsFormSet(instance=product)
		ctx['title'] = 'Detail Output'

		# Passa os dados de cada formulário individualmente para o contexto
		if EstoqueItensFormSet(instance=product):
			for form in EstoqueItensFormSet(instance=product):
				produto_nome = form.instance.product.product if form.instance.product else ''

				ctx['produto_nome'] = produto_nome
		
		return ctx