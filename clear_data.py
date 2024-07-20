import django
import os

# Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque.settings')
django.setup()

from apps.estoque_produtos.models import Inventory, InventoryItems
from apps.produto.models import Products

def clear_data():
	"""
		Clears all data from the database by deleting all instances of `InventoryItems`, `Inventory`, and `Products`.

		This function does not take any parameters and does not return anything.

		Example usage:

		```python
		python3 clear_data()
		```
	"""
	clean_0 = InventoryItems.objects.all().delete()
	clean_1= Inventory.objects.all().delete()
	clean_2 = Products.objects.all().delete()
	
if __name__ == '__main__':
	clear_data()