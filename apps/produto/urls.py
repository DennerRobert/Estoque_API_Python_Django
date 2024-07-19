from django.urls import path
from apps.produto import views

# api produto
from .views import ProductExcelAllView, ProductViewSet


app_name = 'product'

urlpatterns = [
	path('', views.ProductListView.as_view(), name='product_list'),
	path('add/', views.ProductAddView.as_view(), name='product_add'),
	path('<int:pk>/edit/', views.ProductEditView.as_view(), name='product_edit'),
	path('<int:pk>/del/', views.ProductDeleteAjax.as_view(), name='product_delete'),

	path('products/print_current/', views.ProductPrintCurrentView.as_view(), name='product_print_current'),
	path('products/print_all/', views.ProductPrintAllView.as_view(), name='product_print_all'),

    path('export/excel/all/', ProductExcelAllView.as_view(), name='product_excel_all'),
    
	# api produto
	path('list_product/', ProductViewSet.as_view({'get': 'list'}), name='list_product'),
	path('add_product/', ProductViewSet.as_view({'post': 'create'}), name='add_product'),
	path('edit_product/<int:pk>/', ProductViewSet.as_view({'patch': 'update'}), name='edit_product'),
	path('delete_product/<int:pk>/', ProductViewSet.as_view({'delete': 'destroy'}), name='delete_product'),
]