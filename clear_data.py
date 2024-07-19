import django
import os

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.estoque_produtos.models import Inventory, InventoryItems
from apps.produto.models import Products

def clear_data():
	pass
	# Excluir todos os entradas / saídas
	clean_0 = InventoryItems.objects.all().delete()
	clean_1= Inventory.objects.all().delete()
	# --------

	# Excluir todos os Produtos
	clean_2 = Products.objects.all().delete()
	# --------
	
if __name__ == '__main__':
	clear_data()