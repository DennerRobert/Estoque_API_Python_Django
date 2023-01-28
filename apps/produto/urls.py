from django.urls import path
from apps.produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='produto_list'),
    path('add/', views.ProdutoAddView.as_view(), name='produto_add'),
    path('<int:pk>/edit/', views.ProdutoEditView.as_view(), name='produto_edit'),
]