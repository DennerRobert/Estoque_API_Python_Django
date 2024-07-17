from apps.produto.forms import ProdutosForm
from .models import Produtos
from django.views.generic import UpdateView, View, ListView, CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator

# api produto
# from rest_framework.generics import CreateAPIView
from .serializers import ProdutoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class ProdutoListView(ListView):
	model = Produtos
	template_name = 'produtos_list.html'
	context_object_name = 'produtos'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		ctx = super(ProdutoListView, self).get_context_data(**kwargs)
		ctx['query'] = self.request.GET.get('q', '')

		for produto in ctx['produtos']:
			produto.valor_total = produto.estoque * produto.preco

		produtos = Produtos.objects.filter(ativo=True)
		paginator = Paginator(produtos, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['produtos'] = page_obj

		return ctx

	def get_queryset(self, **kwargs):
		queryset = super().get_queryset()
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(produto__icontains=query)
		return queryset.filter(ativo=True).order_by('produto')


class ProdutoAddView(CreateView):
	template_name ='produtos_form.html'
	model = Produtos
	form_class = ProdutosForm
	success_message = 'Produtos adicionado com sucesso'

	def get_context_data(self, **kwargs):
		ctx = super(ProdutoAddView, self).get_context_data(**kwargs)
		ctx['title'] = 'Product Registration'
		return ctx

	def form_valid(self, form):
		produtos_form = form.save(commit=False)
		produtos_form.ativo = True
		produtos_form.produto = produtos_form.produto
		produtos_form.preco = produtos_form.preco
		produtos_form.estoque = 0
		produtos_form.save()
		
		return redirect('produto:produto_list')

class ProdutoEditView(UpdateView):
	model = Produtos
	template_name = 'produtos_form.html'
	form_class = ProdutosForm

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['title'] = 'Edit Product'
		return ctx
	
	def form_valid(self, form):
		produto = form.save()
		return redirect('produto:produto_list')
	

class DispostivosDeleteAjax(View):
	def get(self, request, pk):
		remove_produto = Produtos.objects.filter(pk=pk).first()

		if remove_produto:
			remove_produto.ativo = False
			remove_produto.save()
			messages.success(self.request, self.success_message)  
		else:
			messages.success(self.request, self.error_message) 

		return redirect('produto:produto_list') 
	

class ProdutoViewSet(viewsets.ViewSet):

	serializer_class = ProdutoSerializer

	def list(self, request):
		produtos = Produtos.objects.all()
		serializer = ProdutoSerializer(produtos, many=True)
		return Response(serializer.data)
	

	def create(self, request):
		serializer = ProdutoSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)
	

	def update(self, request, pk=None):
		try:
			produto = Produtos.objects.get(pk=pk)
			serializer = ProdutoSerializer(produto, data=request.data)
			if serializer.is_valid():
				serializer.save()
				# return Response(serializer.data, status=status.HTTP_200_OK)
				return Response(serializer.data,  status=201)
			else:
				# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
				return Response(serializer.errors, status=400)
			
		except produto.DoesNotExist:
			return Response(status=400)
		

	def destroy(self, request, pk, format=None):
		produto = Produtos.objects.get(pk=pk)
		produto.ativo = False
		produto.save()
		# return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(status=201)
    

class ProdutoPrintAtualView(ListView):
	model = Produtos
	template_name = 'produto_print.html'
	context_object_name = 'produtos'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset()
		# filtro com base na query atual
		query = self.request.GET.get('q')
		if query:
			queryset = queryset.filter(produto__icontains=query)
		return queryset
	
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		# cálculo do valor total do estoque no contexto
		for produto in ctx['produtos']:
			produto.valor_total = produto.estoque * produto.preco

		return ctx

class ProdutoPrintTodosView(ListView):
	model = Produtos
	template_name = 'produto_print.html'
	context_object_name = 'produtos'
	paginate_by = None

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)

		for produto in ctx['produtos']:
			produto.valor_total = produto.estoque * produto.preco

		return ctx