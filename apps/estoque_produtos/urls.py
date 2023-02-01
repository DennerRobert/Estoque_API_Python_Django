from django.urls import path
from apps.estoque_produtos import views

app_name = 'estoque_produtos'

urlpatterns = [
    path('', views.EstoqueEntradaList.as_view(), name='estoque_entrada_list'),
]