import django
import os

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.estoque_produtos.models import EstoqueItens, Estoque

def clear_data():
    pass
    # Excluir todos os produtosEstoque
    # EstoqueSaidaList1 = EstoqueItens.objects.all().delete()
    # EstoqueSaidaList1 = Estoque.objects.all().delete()
    # --------
    
    # EstoqueSaidaList1 = Estoque.objects.all()
    # print('-----', EstoqueSaidaList1)
if __name__ == '__main__':
    clear_data()