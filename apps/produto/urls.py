from django.urls import path
from apps.produto import views

app_name = 'produto'

urlpatterns = [
    path('', views.ProdutoListView.as_view(), name='produto_list'),
]