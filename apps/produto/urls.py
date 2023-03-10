from django.urls import path
from apps.produto import views

# api produto
from .views import ProdutoViewSet


app_name = 'produto'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='produto_list'),
    path('add/', views.ProdutoAddView.as_view(), name='produto_add'),
    path('<int:pk>/edit/', views.ProdutoEditView.as_view(), name='produto_edit'),
    path('<int:pk>/del/', views.DispostivosDeleteAjax.as_view(), name='produto_delete'),

    # api produto
    path('listar_produto/', ProdutoViewSet.as_view({'get': 'list'}), name='listar_produto'),
    path('adicionar_produto/', ProdutoViewSet.as_view({'post': 'create'}), name='adicionar_produto'),
    path('editar_produto/<int:pk>/', ProdutoViewSet.as_view({'patch': 'update'}), name='editar_produto'),
    path('deletar_produto/<int:pk>/', ProdutoViewSet.as_view({'delete': 'destroy'}), name='deletar_produto'),
]