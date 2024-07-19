import random
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.produto.models import Products

nomes_produtos = [
	'Arroz Integral', 'Óleo de Soja', 'Farinha de Trigo', 'Feijão Carioca', 'Leite Integral',
	'Macarrão Espaguete', 'Sabão em Pó', 'Detergente Líquido', 'Shampoo Anticaspa', 'Condicionador Hidratante',
	'Café Torrado e Moído', 'Açúcar Cristal', 'Sal Refinado', 'Suco de Laranja Natural', 'Biscoito Recheado',
	'Creme Dental com Flúor', 'Desodorante Roll-On', 'Papel Higiênico Folha Dupla', 'Chocolate ao Leite', 'Refrigerante de Guaraná'
]

def adicionar_produtos():
	for nome in nomes_produtos:
		quantidade = random.randint(10, 100)
		preco = round(random.uniform(10.0, 100.0), 2)

		produto = Products.objects.create(
			product=nome,
			price=preco,
			inventory=quantidade,
		)
		print(f"Produto '{produto.product}' adicionado com sucesso.")

if __name__ == '__main__':
	adicionar_produtos()
