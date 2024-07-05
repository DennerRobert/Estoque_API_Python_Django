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
    # clean = EstoqueItens.objects.all().delete()
    # clean_1 = Estoque.objects.all().delete()
    # --------

    # Excluir todos os Produtos
    # clean = Produtos.objects.all().delete()
    # --------
    
    # clean = Produtos.objects.all()
    # print('-----', clean) 
if __name__ == '__main__':
    clear_data()