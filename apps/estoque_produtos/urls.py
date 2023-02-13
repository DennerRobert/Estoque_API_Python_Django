from django.urls import path

from apps.estoque_produtos import views
from .views import get_saldo_ajax

app_name = 'estoque_produtos'

urlpatterns = [
    path('', views.EstoqueEntradaList.as_view(), name='estoque_entrada_list'),
    path('add/', views.add_estoque.as_view(), name='estoque_entrada_add'),
    path('list/', views.EstoqueSaidaList.as_view(), name='estoque_saida_list'),
    path('saida/', views.del_estoque.as_view(), name='estoque_saida'),

    path('<int:pk>/up/', views.up_estoque.as_view(), name='estoque_entrada_up'),

    path('get_saldo_ajax/', get_saldo_ajax, name='get_saldo_ajax'),
]