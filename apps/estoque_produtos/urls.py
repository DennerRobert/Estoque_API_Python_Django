from django.urls import path

from apps.estoque_produtos import views
from .views import produto_saldo

app_name = 'estoque_produtos'

urlpatterns = [
	path('', views.StockEntryListView.as_view(), name='stock_entry_list'),
	path('add/', views.StockEntryCreateView.as_view(), name='stock_entry_add'),
	path('list/', views.StockOutputListView.as_view(), name='stock_output_list'),
	path('output/', views.StockOutputCreateView.as_view(), name='stock_output_add'),

	path('<int:pk>/update/', views.StockUpdateView.as_view(), name='stock_update'),

	path('<int:pk>/detail/en', views.StockEntryDetailView.as_view(), name='stock_entry_detail'),
	path('<int:pk>/detail/ex/', views.StockOutputDetailView.as_view(), name='detail_stock_exit'),

	path('estoque_produtos/<int:produto_id>/saldo/', produto_saldo, name='produto_saldo'),
]