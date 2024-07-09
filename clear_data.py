import django
import os

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.estoque_produtos.models import EstoqueItens, Estoque
from apps.produto.models import Produtos

def clear_data():
    pass
    # Excluir todos os entradas / saídas
    # clean_0 = EstoqueItens.objects.all().delete()
    # clean_1= Estoque.objects.all().delete()
    # --------

    # Excluir todos os Produtos
    # clean_2 = Produtos.objects.all().delete()
    # --------
    
if __name__ == '__main__':
    clear_data()