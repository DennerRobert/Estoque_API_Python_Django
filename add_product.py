import random
import django
import os

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.produto.models import Produtos

# Lista de nomes de produtos predefinidos
nomes_produtos = [
    'Produto 1', 'Produto 2', 'Produto 3', 'Produto 4', 'Produto 5',
    'Produto 6', 'Produto 7', 'Produto 8', 'Produto 9', 'Produto 10',
    'Produto 11', 'Produto 12', 'Produto 13', 'Produto 14', 'Produto 15',
    'Produto 16', 'Produto 17', 'Produto 18', 'Produto 19', 'Produto 20',
]

def adicionar_produtos():
    for nome in nomes_produtos:
        quantidade = random.randint(10, 100)  # Quantidade aleatória entre 10 e 100
        preco = round(random.uniform(10.0, 100.0), 2)  # Preço aleatório entre 10.0 e 100.0, arredondado para 2 casas decimais

        produto = Produtos.objects.create(
            produto=nome,
            preco=preco,
            estoque=quantidade,
        )
        print(f"Produto '{produto.produto}' adicionado com sucesso.")

if __name__ == '__main__':
    adicionar_produtos()
