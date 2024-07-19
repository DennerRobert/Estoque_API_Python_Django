from datetime import datetime
from apps.produto.forms import ProductsForm
from .models import Products
from django.views.generic import UpdateView, View, ListView, CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
import openpyxl
from django.http import HttpResponse

# api produto
# from rest_framework.generics import CreateAPIView
from .serializers import ProductSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


class ProductListView(ListView):
	model = Products
	template_name = 'product_list.html'
	context_object_name = 'products'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		ctx = super(ProductListView, self).get_context_data(**kwargs)
		ctx['query'] = self.request.GET.get('q', '')

		for product in ctx['products']:
			product.total_value = product.inventory * product.price

		products = Products.objects.filter(active=True)
		paginator = Paginator(products, self.paginate_by)
		page_number = self.request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		ctx['products'] = page_obj

		return ctx

	def get_queryset(self, **kwargs):
		queryset = super().get_queryset()
		query = self.request.GET.get('q')
		
		if query:
			queryset = queryset.filter(product__icontains=query)
		
		return queryset.filter(active=True).order_by('product')



class ProductAddView(CreateView):
	template_name = 'product_form.html'
	model = Products
	form_class = ProductsForm
	success_message = 'Product added successfully'

	def get_context_data(self, **kwargs):
		ctx = super(ProductAddView, self).get_context_data(**kwargs)
		ctx['title'] = 'Product Registration'
		return ctx

	def form_valid(self, form):
		product_form = form.save(commit=False)
		product_form.active = True
		product_form.product = product_form.product
		product_form.price = product_form.price
		product_form.inventory = 0
		product_form.save()
		
		return redirect('product:product_list')

class ProductEditView(UpdateView):
	model = Products
	template_name = 'product_form.html'
	form_class = ProductsForm

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['title'] = 'Edit Product'
		return ctx
	
	def form_valid(self, form):
		product = form.save()
		return redirect('product:product_list')

	

class ProductDeleteAjax(View):
	def get(self, request, pk):
		remove_product = Products.objects.filter(pk=pk).first()

		if remove_product:
			remove_product.active = False
			remove_product.save()
		else:
			messages.error(self.request, self.error_message) 

		return redirect('product:product_list')

	
# api produto
class ProductViewSet(viewsets.ViewSet):

	serializer_class = ProductSerializer

	def list(self, request):
		products = Products.objects.all()
		serializer = ProductSerializer(products, many=True)
		return Response(serializer.data)
	

	def create(self, request):
		serializer = ProductSerializer(data=request.data)
		
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)
	

	def update(self, request, pk=None):
		try:
			products = Products.objects.get(pk=pk)
			serializer = ProductSerializer(products, data=request.data)
			
			if serializer.is_valid():
				serializer.save()
				# return Response(serializer.data, status=status.HTTP_200_OK)
				return Response(serializer.data,  status=201)
			else:
				# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
				return Response(serializer.errors, status=400)
			
		except products.DoesNotExist:
			return Response(status=400)
		

	def destroy(self, request, pk, format=None):
		products = Products.objects.get(pk=pk)
		products.active = False
		products.save()
		# return Response(status=status.HTTP_204_NO_CONTENT)
		return Response(status=201)
	

# print product list
class ProductPrintCurrentView(ListView):
	model = Products
	template_name = 'product_print.html'
	context_object_name = 'products'
	paginate_by = 10

	def get_queryset(self):
		queryset = super().get_queryset()
		# filtro com base na query atual
		query = self.request.GET.get('q')
		
		if query:
			queryset = queryset.filter(active=True, product__icontains=query)
		
		return queryset
	
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		# cálculo do valor total do estoque no contexto
		for product in ctx['products']:
			product.valor_total = product.inventory * product.price

		user = self.request.user
		date = datetime.now().strftime('%d-%m-%Y - %H:%M')
		ctx['user']	= user 
		ctx['date']	= date 
		
		return ctx


# print product list - todos os itens
class ProductPrintAllView(ListView):
	model = Products
	template_name = 'product_print.html'
	context_object_name = 'products'
	paginate_by = None

	def get_queryset(self):
		queryset = super().get_queryset()
		queryset = queryset.filter(active=True)

		return queryset
	
	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)

		for product in ctx['products']:
			product.valor_total = product.inventory * product.price

		user = self.request.user
		date = datetime.now().strftime('%d-%m-%Y - %H:%M')
		ctx['user']	= user 
		ctx['date']	= date 
		
		return ctx
	

# exportar para excel
class ExportProductExcelView(ListView):
	model = Products

	def get_queryset(self):
		queryset = super().get_queryset()
		query = self.request.GET.get('q')
		
		if query:
			queryset = queryset.filter(product__icontains=query)
		
		return queryset

	def export_to_excel(self, queryset, filename):
		workbook = openpyxl.Workbook()
		sheet = workbook.active
		sheet.title = "Products"

		headers = ['ID', 'Product', 'Price', 'Stock', 'Total Balance']
		sheet.append(headers)

		for index, product in enumerate(queryset, start=1):
			row = [
				index,
				product.product.upper(),
				product.price,
				product.inventory,
				product.inventory * product.price
			]
			sheet.append(row)

		response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
		response['Content-Disposition'] = f'attachment; filename={filename}.xlsx'
		workbook.save(response)
		
		return response


# exportar para excel todos os itens ativos
class ProductExcelAllView(ExportProductExcelView):
	def get(self, request, *args, **kwargs):
		queryset = Products.objects.filter(active=True)
		
		return self.export_to_excel(queryset, 'complete_products')